import unittest
from unittest.mock import patch, MagicMock
import io
import sys
import subprocess
import hadoop_checker as hadoop  # Replace with your module name

class TestHadoopHealthChecker(unittest.TestCase):

    def setUp(self):
        """
        Create a reusable instance of the HadoopHealthChecker for all tests.
        """
        self.checker = hadoop.HadoopHealthChecker()

    @patch('subprocess.check_output')
    def test_get_hadoop_version_success(self, mock_subprocess):
        """
        Test successful retrieval of Hadoop version.
        """
        mock_subprocess.return_value = b"Hadoop 3.3.4\nAdditional info"
        self.assertEqual(self.checker.get_hadoop_version(), "3.3.4")

    @patch('subprocess.check_output')
    def test_get_hadoop_version_error(self, mock_subprocess):
        """
        Test handling of error during Hadoop version retrieval.
        """
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, 'hadoop version')
        self.assertEqual(self.checker.get_hadoop_version(), "unknown")

    @patch('subprocess.check_output')
    def test_check_hadoop_status(self, mock_subprocess):
        """
        Test handling of different Hadoop health statuses.
        """
        scenarios = [
            (b'{"status": "GOOD", "message": "Healthy"}', hadoop.HadoopHealthChecker.OK, "healthy"),
            (b'{"status": "CONCERNING", "message": "Some issue"}', hadoop.HadoopHealthChecker.WARNING, "concerning"),
            (b'{"status": "BAD", "message": "Critical problem"}', hadoop.HadoopHealthChecker.CRITICAL, "bad state"),
            (b'{"status": "UNKNOWN", "message": "No information"}', hadoop.HadoopHealthChecker.UNKNOWN, "unknown state"),
        ]

        for response, expected_status, expected_message in scenarios:
            mock_subprocess.return_value = response
            status, message = self.checker.check_hadoop()
            self.assertEqual(status, expected_status)
            self.assertIn(expected_message, message.lower())

    @patch('subprocess.check_output')
    def test_check_hadoop_error_handling(self, mock_subprocess):
        """
        Test handling of errors during 'hadoop health' check.
        """
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, 'hadoop health')
        status, message = self.checker.check_hadoop()
        self.assertEqual(status, hadoop.HadoopHealthChecker.UNKNOWN)
        self.assertIn("error running", message.lower())

    @patch('subprocess.check_output')
    def test_check_hdfs_capacity(self, mock_subprocess):
        """
        Test HDFS capacity check with varying usage levels.
        """
        scenarios = [
            (b"DFS Used%: 50%\n", hadoop.HadoopHealthChecker.OK, "capacity"),
            (b"DFS Used%: 95%\n", hadoop.HadoopHealthChecker.CRITICAL, "capacity is critical"),  # Changed to CRITICAL
            (b"DFS Used%: 85%\n", hadoop.HadoopHealthChecker.WARNING, "capacity is high"),
        ]

        for response, expected_status, expected_message in scenarios:
            mock_subprocess.return_value = response
            status, message = self.checker.check_hdfs_capacity()
            self.assertEqual(status, expected_status)
            self.assertIn(expected_message, message.lower())

    @patch('subprocess.check_output')
    def test_check_hdfs_capacity_error(self, mock_subprocess):
        """
        Test handling of errors during HDFS capacity check.
        """
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, 'hdfs dfsadmin -report')
        status, message = self.checker.check_hdfs_capacity()
        self.assertEqual(status, hadoop.HadoopHealthChecker.UNKNOWN)
        self.assertIn("error checking hdfs capacity", message.lower())

    @patch('subprocess.check_output')
    def test_check_datanode_status(self, mock_subprocess):
        """
        Test DataNode status check with different scenarios.
        """
        scenarios = [
            (b"Live datanodes: 3\n", hadoop.HadoopHealthChecker.OK, "live datanodes found"),
            (b"Live datanodes: 0\n", hadoop.HadoopHealthChecker.CRITICAL, "no live datanodes found"),
        ]

        for response, expected_status, expected_message in scenarios:
            mock_subprocess.return_value = response
            status, message = self.checker.check_datanode_status()
            self.assertEqual(status, expected_status)
            self.assertIn(expected_message, message.lower())

    @patch('subprocess.check_output')
    def test_check_datanode_status_error(self, mock_subprocess):
        """
        Test handling of errors during DataNode status check.
        """
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, 'hdfs dfsadmin -report')
        status, message = self.checker.check_datanode_status()
        self.assertEqual(status, hadoop.HadoopHealthChecker.UNKNOWN)
        self.assertIn("error checking datanode status", message.lower())

    def test_format_output(self):
        """
        Test the format_output method for correctness.
        """
        formatted_output = self.checker.format_output("OK", "Test message")
        self.assertEqual(formatted_output, "OK - Test message")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('hadoop_checker.HadoopHealthChecker.check_hadoop', return_value=("OK", "Hadoop is healthy"))
    @patch('hadoop_checker.HadoopHealthChecker.check_hdfs_capacity', return_value=("OK", "HDFS is healthy"))
    @patch('hadoop_checker.HadoopHealthChecker.check_datanode_status', return_value=("OK", "DataNodes are healthy"))
    def test_main_verbose(self, mock_datanode, mock_hdfs, mock_hadoop, mock_stdout):
        """
        Test main function with verbose output.
        """
        sys.argv = ["hadoop_checker.py", "--verbose"]
        with self.assertRaises(SystemExit) as cm:
            hadoop.main()
        self.assertEqual(cm.exception.code, 0)
        output = mock_stdout.getvalue().lower()
        self.assertIn("hadoop is healthy", output)
        self.assertIn("hdfs is healthy", output)
        self.assertIn("datanodes are healthy", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('hadoop_checker.HadoopHealthChecker.check_hadoop', return_value=("OK", "Hadoop is healthy"))
    def test_main_non_verbose(self, mock_hadoop, mock_stdout):
        """
        Test main function without verbose output.
        """
        sys.argv = ["hadoop_checker.py"]
        with self.assertRaises(SystemExit) as cm:
            hadoop.main()
        self.assertEqual(cm.exception.code, 0)
        output = mock_stdout.getvalue().lower()
        self.assertNotIn("hadoop version", output)

    @patch('subprocess.check_output')
    def test_invalid_hadoop_output(self, mock_subprocess):
        """
        Test handling of invalid output format from Hadoop commands.
        """
        # Simulate a non-JSON response
        mock_subprocess.return_value = b"Invalid Output"  
        status, message = self.checker.check_hadoop()
        self.assertEqual(status, hadoop.HadoopHealthChecker.UNKNOWN)
        self.assertIn("error decoding json", message.lower())

    @patch('subprocess.check_output')
    def test_missing_keys_in_json(self, mock_subprocess):
        """
        Test handling of missing keys in JSON response.
        """
        # Simulate a response missing the 'status' key
        mock_subprocess.return_value = b'{"message": "Some message"}' 
        status, message = self.checker.check_hadoop()
        self.assertEqual(status, hadoop.HadoopHealthChecker.UNKNOWN)  # Should default to UNKNOWN

    @patch('subprocess.check_output')
    def test_hdfs_capacity_parsing_error(self, mock_subprocess):
        """
        Test handling of unexpected output format from 'hdfs dfsadmin -report'.
        """
        # Simulate output that doesn't contain "DFS Used%"
        mock_subprocess.return_value = b"Some unexpected output"
        status, message = self.checker.check_hdfs_capacity()
        self.assertEqual(status, hadoop.HadoopHealthChecker.UNKNOWN)
        self.assertIn("could not determine hdfs capacity", message.lower())

    @patch('subprocess.check_output')
    def test_datanode_status_parsing_error(self, mock_subprocess):
        """
        Test handling of unexpected output format from 'hdfs dfsadmin -report'.
        """
        # Simulate output that doesn't contain "Live datanodes"
        mock_subprocess.return_value = b"Some unexpected output"
        status, message = self.checker.check_datanode_status()
        self.assertEqual(status, hadoop.HadoopHealthChecker.UNKNOWN)
        self.assertIn("could not determine live datanodes", message.lower())


if __name__ == '__main__':
    unittest.main()
