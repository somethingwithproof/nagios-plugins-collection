import unittest
import hadoop
from unittest.mock import patch, MagicMock

class TestHadoop(unittest.TestCase):

    def test_help(self):
        """
        Test that the help function exits with status code 3
        """
        with self.assertRaises(SystemExit) as cm:
            hadoop.help()
        self.assertEqual(cm.exception.code, 3)

    @patch('urllib.request.urlopen')
    def test_main_ok_status(self, mock_urlopen):
        """
        Test that the main function exits with status code 0 when the JSON API returns an "ok" status
        """
        mock_urlopen.return_value = MagicMock(read=lambda: b'{"status":"ok", "subcomponents":[{"status":"ok", "name":"component1", "updated":"2022-01-01 00:00:00", "message":""}]}')
        with self.assertRaises(SystemExit) as cm:
            hadoop.main()
        self.assertEqual(cm.exception.code, 0)

    @patch('urllib.request.urlopen')
    def test_main_bad_status(self, mock_urlopen):
        """
        Test that the main function exits with status code 1 when the JSON API returns a non "ok" status
        """
        mock_urlopen.return_value = MagicMock(read=lambda: b'{"status":"bad", "subcomponents":[{"status":"ok", "name":"component1", "updated":"2022-01-01 00:00:00", "message":""}]}')
        with self.assertRaises(SystemExit) as cm:
            hadoop.main()
        self.assertEqual(cm.exception.code, 1)

    @patch('urllib.request.urlopen')
    def test_main_bad_subcomponent_status(self, mock_urlopen):
        """
        Test that the main function exits with status code 2 when a subcomponent of the JSON API returns a non "ok" status
        """
        mock_urlopen.return_value = MagicMock(read=lambda: b'{"status":"ok", "subcomponents":[{"status":"bad", "name":"component1", "updated":"2022-01-01 00:00:00", "message":""}]}')
        with self.assertRaises(SystemExit) as cm:
            hadoop.main()
        self.assertEqual(cm.exception.code, 2)

    @patch('urllib.request.urlopen')
    def test_main_time_check(self, mock_urlopen):
        """
        Test that the main function exits with status code 1 when the -t argument is provided and the time since the last update of a subcomponent exceeds the specified value
        """
        mock_urlopen.return_value = MagicMock(read=lambda: b'{"status":"ok", "subcomponents":[{"status":"ok", "name":"component1", "updated":"2010-01-01 00:00:00", "message":""}]}')
        sys.argv = ["hadoop.py", "-
        sys.argv = ["hadoop.py", "-url=test.com", "-t=10"]
        with self.assertRaises(SystemExit) as cm:
            hadoop.main()
        self.assertEqual(cm.exception.code, 1)

    @patch('urllib.request.urlopen')
    def test_main_no_url_provided(self, mock_urlopen):
        """
        Test that the main function exits with status code 3 when no URL is provided
        """
        mock_urlopen.return_value = MagicMock(read=lambda: b'{"status":"ok", "subcomponents":[{"status":"ok", "name":"component1", "updated":"2010-01-01 00:00:00", "message":""}]}')
        sys.argv = ["hadoop.py"]
        with self.assertRaises(SystemExit) as cm:
            hadoop.main()
        self.assertEqual(cm.exception.code, 3)

    @patch('urllib.request.urlopen')
    def test_main_invalid_url(self, mock_urlopen):
        """
        Test that the main function exits with status code 2 when an invalid URL is provided
        """
        mock_urlopen.side_effect = urllib.error.URLError("Invalid URL")
        sys.argv = ["hadoop.py", "-url=invalid.com"]
        with self.assertRaises(SystemExit) as cm:
            hadoop.main()
        self.assertEqual(cm.exception.code, 2)

    @patch('urllib.request.urlopen')
    def test_main_invalid_json(self, mock_urlopen):
        """
        Test that the main function exits with status code 2 when an invalid JSON is returned from the URL
        """
        mock_urlopen.return_value = MagicMock(read=lambda: b'{"status":"ok", "subcomponents":[{"status":"ok", "name":"component1", "updated":"2010-01-01 00:00:00", "message":""}')
        sys.argv = ["hadoop.py", "-url=test.com"]
        with self.assertRaises(SystemExit) as cm:
            hadoop.main()
        self.assertEqual(cm.exception.code, 2)

class TestIntegration(unittest.TestCase):

    def test_integration(self):
        """
        Test that the script works as expected when run with valid command line arguments and a valid JSON API
        """
        sys.argv = ["hadoop.py", "-url=http://test.com"]
        with self.assertRaises(SystemExit) as cm:
            hadoop.main()
        self.assertEqual(cm.exception.code, 0)
