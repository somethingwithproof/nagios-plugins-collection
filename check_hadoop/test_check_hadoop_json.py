import unittest
from unittest.mock import patch, MagicMock
import hadoop_checker
import sys

class TestHadoopChecker(unittest.TestCase):

    @patch('subprocess.check_output')
    def test_get_hadoop_version(self, mock_subprocess):
        mock_subprocess.return_value = "Hadoop 3.3.0\n".encode('utf-8')
        checker = hadoop_checker.HadoopHealthChecker()
        self.assertEqual(checker.get_hadoop_version(), "3.3.0")

    @patch('subprocess.check_output')
    def test_check_hadoop_ok(self, mock_subprocess):
        mock_subprocess.return_value = '{"status": "GOOD", "message": "All systems operational"}'.encode('utf-8')
        checker = hadoop_checker.HadoopHealthChecker()
        status, message = checker.check_hadoop()
        self.assertEqual(status, checker.OK)
        self.assertIn("All systems operational", message)

    @patch('subprocess.check_output')
    def test_check_hadoop_bad(self, mock_subprocess):
        mock_subprocess.return_value = '{"status": "BAD", "message": "Critical issues detected"}'.encode('utf-8')
        checker = hadoop_checker.HadoopHealthChecker()
        status, message = checker.check_hadoop()
        self.assertEqual(status, checker.CRITICAL)
        self.assertIn("Critical issues detected", message)

    @patch('subprocess.check_output')
    def test_check_hdfs_capacity_warning(self, mock_subprocess):
        mock_subprocess.return_value = "DFS Used%: 85.0%\n".encode('utf-8')
        checker = hadoop_checker.HadoopHealthChecker(hdfs_warning=80, hdfs_critical=90)
        status, message = checker.check_hdfs_capacity()
        self.assertEqual(status, checker.WARNING)
        self.assertIn("85.0% used", message)

    @patch('subprocess.check_output')
    def test_check_hdfs_capacity_critical(self, mock_subprocess):
        mock_subprocess.return_value = "DFS Used%: 95.0%\n".encode('utf-8')
        checker = hadoop_checker.HadoopHealthChecker(hdfs_warning=80, hdfs_critical=90)
        status, message = checker.check_hdfs_capacity()
        self.assertEqual(status, checker.CRITICAL)
        self.assertIn("95.0% used", message)

    @patch('subprocess.check_output')
    def test_check_datanode_status_ok(self, mock_subprocess):
        mock_subprocess.return_value = "Live datanodes: 10\n".encode('utf-8')
        checker = hadoop_checker.HadoopHealthChecker()
        status, message = checker.check_datanode_status()
        self.assertEqual(status, checker.OK)
        self.assertIn("10 live DataNodes found", message)

    @patch('subprocess.check_output')
    def test_check_datanode_status_critical(self, mock_subprocess):
        mock_subprocess.return_value = "Live datanodes: 0\n".encode('utf-8')
        checker = hadoop_checker.HadoopHealthChecker()
        status, message = checker.check_datanode_status()
        self.assertEqual(status, checker.CRITICAL)
        self.assertIn("No live DataNodes found", message)

    @patch('subprocess.check_output')
    def test_invalid_json(self, mock_subprocess):
        mock_subprocess.return_value = "{invalid_json".encode('utf-8')
        checker = hadoop_checker.HadoopHealthChecker()
        status, message = checker.check_hadoop()
        self.assertEqual(status, checker.UNKNOWN)
        self.assertIn("Error decoding JSON", message)

    @patch('subprocess.check_output', side_effect=FileNotFoundError)
    def test_missing_hadoop_command(self, mock_subprocess):
        checker = hadoop_checker.HadoopHealthChecker()
        status, message = checker.check_hadoop()
        self.assertEqual(status, checker.UNKNOWN)
        self.assertIn("command not found", message)


class TestCommandLineIntegration(unittest.TestCase):

    @patch('hadoop_checker.HadoopHealthChecker.check_hadoop', return_value=('OK', 'Hadoop is healthy'))
    @patch('hadoop_checker.HadoopHealthChecker.check_hdfs_capacity', return_value=('OK', 'HDFS is healthy'))
    @patch('hadoop_checker.HadoopHealthChecker.check_datanode_status', return_value=('OK', 'DataNodes are healthy'))
    def test_integration_all_checks_ok(self, mock_check_hadoop, mock_check_hdfs, mock_check_datanodes):
        sys.argv = ["hadoop_checker.py", "--check", "all"]
        with self.assertRaises(SystemExit) as cm:
            hadoop_checker.main()
        self.assertEqual(cm.exception.code, 0)

    @patch('hadoop_checker.HadoopHealthChecker.check_hdfs_capacity', return_value=('CRITICAL', 'HDFS capacity exceeded'))
    def test_integration_hdfs_critical(self, mock_check_hdfs):
        sys.argv = ["hadoop_checker.py", "--check", "hdfs"]
        with self.assertRaises(SystemExit) as cm:
            hadoop_checker.main()
        self.assertEqual(cm.exception.code, 2)

    @patch('hadoop_checker.HadoopHealthChecker.check_datanode_status', return_value=('WARNING', 'Few live DataNodes'))
    def test_integration_datanodes_warning(self, mock_check_datanodes):
        sys.argv = ["hadoop_checker.py", "--check", "datanode"]
        with self.assertRaises(SystemExit) as cm:
            hadoop_checker.main()
        self.assertEqual(cm.exception.code, 1)


if __name__ == '__main__':
    unittest.main()
