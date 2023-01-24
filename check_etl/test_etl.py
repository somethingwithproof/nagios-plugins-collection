import unittest
from unittest.mock import patch
import argparse
import json
import urllib.request
import urllib.error
import datetime
from component_checker import main, parse_args, component_checker

class TestMain(unittest.TestCase):
    def test_main_ok(self):
        with patch('component_checker.component_checker') as mocked_component_checker:
            mocked_component_checker.return_value = ('ok', datetime.timedelta(minutes=10))
            args = parse_args(['-url=example.com', '-component=component1', '-t=30'])
            result = main(args)
            self.assertEqual(result, 0)

    def test_main_warning(self):
        with patch('component_checker.component_checker') as mocked_component_checker:
            mocked_component_checker.return_value = ('ok', datetime.timedelta(minutes=40))
            args = parse_args(['-url=example.com', '-component=component1', '-t=30'])
            result = main(args)
            self.assertEqual(result, 1)

    def test_main_error(self):
        with patch('component_checker.component_checker') as mocked_component_checker:
            mocked_component_checker.return_value = ('error', 'something went wrong')
            args = parse_args(['-url=example.com', '-component=component1', '-t=30'])
            result = main(args)
            self.assertEqual(result, 2)
