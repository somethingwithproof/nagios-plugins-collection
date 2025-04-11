#!/usr/bin/env python3
"""
Unit tests for the modernized Hadoop health check plugin.

This module contains unit tests for the check_hadoop_modernized.py module.
It tests the functionality of the various health checks and ensures they
return the expected results.
"""

import asyncio
import json
import subprocess
import unittest
from unittest.mock import patch, MagicMock

import httpx

from check_hadoop_modernized import (
    Status,
    CheckResult,
    HadoopVersionCheck,
    HadoopHealthCommandCheck,
    HDFSCapacityCheck,
    DataNodeStatusCheck,
    APIHealthCheck,
    HealthCheckRunner,
    OutputFormatter,
)


class TestStatus(unittest.TestCase):
    """Test the Status enum."""

    def test_status_values(self):
        """Test that the Status enum has the correct values."""
        self.assertEqual(Status.OK.value, 0)
        self.assertEqual(Status.WARNING.value, 1)
        self.assertEqual(Status.CRITICAL.value, 2)
        self.assertEqual(Status.UNKNOWN.value, 3)

    def test_status_string_representation(self):
        """Test the string representation of Status enum values."""
        self.assertEqual(str(Status.OK), "OK")
        self.assertEqual(str(Status.WARNING), "WARNING")
        self.assertEqual(str(Status.CRITICAL), "CRITICAL")
        self.assertEqual(str(Status.UNKNOWN), "UNKNOWN")


class TestCheckResult(unittest.TestCase):
    """Test the CheckResult class."""

    def test_check_result_string_representation(self):
        """Test the string representation of CheckResult."""
        # Basic result
        result = CheckResult(Status.OK, "All good")
        self.assertEqual(str(result), "OK - All good")

        # Result with metrics
        result = CheckResult(
            Status.WARNING, "High usage", metrics={"usage": 85, "limit": 100}
        )
        self.assertEqual(str(result), "WARNING - High usage | usage=85 limit=100")

        # Result with details
        result = CheckResult(
            Status.CRITICAL,
            "Service down",
            metrics={"uptime": 0},
            details="Service crashed at 14:30",
        )
        self.assertEqual(
            str(result),
            "CRITICAL - Service down | uptime=0\nService crashed at 14:30",
        )

    def test_check_result_to_json(self):
        """Test the to_json method of CheckResult."""
        result = CheckResult(
            Status.WARNING,
            "High usage",
            metrics={"usage": 85, "limit": 100},
            details="Approaching limit",
        )
        json_str = result.to_json()
        json_data = json.loads(json_str)

        self.assertEqual(json_data["status"], "WARNING")
        self.assertEqual(json_data["message"], "High usage")
        self.assertEqual(json_data["metrics"], {"usage": 85, "limit": 100})
        self.assertEqual(json_data["details"], "Approaching limit")


class TestHadoopVersionCheck(unittest.TestCase):
    """Test the HadoopVersionCheck class."""

    def setUp(self):
        """Set up the test case."""
        self.check = HadoopVersionCheck()

    def test_name_property(self):
        """Test the name property."""
        self.assertEqual(self.check.name, "hadoop_version")

    @patch("check_hadoop_modernized.CommandHealthCheck.execute_command")
    async def test_check_success(self, mock_execute):
        """Test successful version check."""
        mock_execute.return_value = "Hadoop 3.3.4\nCompiled by ...\n"
        result = await self.check.check()

        self.assertEqual(result.status, Status.OK)
        self.assertEqual(result.message, "Hadoop version: 3.3.4")
        self.assertEqual(result.metrics, {"version": "3.3.4"})

    @patch("check_hadoop_modernized.CommandHealthCheck.execute_command")
    async def test_check_error(self, mock_execute):
        """Test error handling in version check."""
        mock_execute.side_effect = subprocess.SubprocessError("Command failed")
        result = await self.check.check()

        self.assertEqual(result.status, Status.UNKNOWN)
        self.assertTrue("Error fetching Hadoop version" in result.message)


class TestHadoopHealthCommandCheck(unittest.TestCase):
    """Test the HadoopHealthCommandCheck class."""

    def setUp(self):
        """Set up the test case."""
        self.check = HadoopHealthCommandCheck()

    def test_name_property(self):
        """Test the name property."""
        self.assertEqual(self.check.name, "hadoop_health")

    @patch("check_hadoop_modernized.CommandHealthCheck.execute_command")
    async def test_check_good_status(self, mock_execute):
        """Test health check with GOOD status."""
        mock_execute.return_value = json.dumps({
            "status": "GOOD",
            "message": "Hadoop is healthy",
            "uptime": 3600,
            "nodes": 5
        })
        result = await self.check.check()

        self.assertEqual(result.status, Status.OK)
        self.assertEqual(result.message, "Hadoop is healthy")
        self.assertEqual(result.metrics, {"uptime": 3600, "nodes": 5})

    @patch("check_hadoop_modernized.CommandHealthCheck.execute_command")
    async def test_check_concerning_status(self, mock_execute):
        """Test health check with CONCERNING status."""
        mock_execute.return_value = json.dumps({
            "status": "CONCERNING",
            "message": "High resource usage",
            "uptime": 3600,
            "nodes": 5
        })
        result = await self.check.check()

        self.assertEqual(result.status, Status.WARNING)
        self.assertEqual(result.message, "High resource usage")

    @patch("check_hadoop_modernized.CommandHealthCheck.execute_command")
    async def test_check_bad_status(self, mock_execute):
        """Test health check with BAD status."""
        mock_execute.return_value = json.dumps({
            "status": "BAD",
            "message": "Service degraded",
            "uptime": 3600,
            "nodes": 3
        })
        result = await self.check.check()

        self.assertEqual(result.status, Status.CRITICAL)
        self.assertEqual(result.message, "Service degraded")

    @patch("check_hadoop_modernized.CommandHealthCheck.execute_command")
    async def test_check_json_decode_error(self, mock_execute):
        """Test health check with invalid JSON response."""
        mock_execute.return_value = "Not a JSON"
        result = await self.check.check()

        self.assertEqual(result.status, Status.UNKNOWN)
        self.assertTrue("Error decoding JSON" in result.message)

    @patch("check_hadoop_modernized.CommandHealthCheck.execute_command")
    async def test_check_command_error(self, mock_execute):
        """Test health check with command execution error."""
        mock_execute.side_effect = subprocess.SubprocessError("Command failed")
        result = await self.check.check()

        self.assertEqual(result.status, Status.UNKNOWN)
        self.assertTrue("Error checking Hadoop health" in result.message)


class TestHDFSCapacityCheck(unittest.TestCase):
    """Test the HDFSCapacityCheck class."""

    def setUp(self):
        """Set up the test case."""
        self.check = HDFSCapacityCheck(warning_threshold=80, critical_threshold=90)

    def test_name_property(self):
        """Test the name property."""
        self.assertEqual(self.check.name, "hdfs_capacity")

    def test_init_with_thresholds(self):
        """Test initialization with custom thresholds."""
        check = HDFSCapacityCheck(warning_threshold=75, critical_threshold=85)
        self.assertEqual(check.warning_threshold, 75)
        self.assertEqual(check.critical_threshold, 85)

    @patch("check_hadoop_modernized.CommandHealthCheck.execute_command")
    async def test_check_ok_status(self, mock_execute):
        """Test capacity check with OK status."""
        mock_execute.return_value = "DFS Used%: 50%\n"
        result = await self.check.check()

        self.assertEqual(result.status, Status.OK)
        self.assertEqual(result.message, "HDFS capacity: 50.0% used")
        self.assertEqual(result.metrics, {"capacity_used_percent": 50.0})

    @patch("check_hadoop_modernized.CommandHealthCheck.execute_command")
    async def test_check_warning_status(self, mock_execute):
        """Test capacity check with WARNING status."""
        mock_execute.return_value = "DFS Used%: 85%\n"
        result = await self.check.check()

        self.assertEqual(result.status, Status.WARNING)
        self.assertEqual(result.message, "HDFS capacity is warning: 85.0% used")
        self.assertEqual(result.metrics, {"capacity_used_percent": 85.0})

    @patch("check_hadoop_modernized.CommandHealthCheck.execute_command")
    async def test_check_critical_status(self, mock_execute):
        """Test capacity check with CRITICAL status."""
        mock_execute.return_value = "DFS Used%: 95%\n"
        result = await self.check.check()

        self.assertEqual(result.status, Status.CRITICAL)
        self.assertEqual(result.message, "HDFS capacity is critical: 95.0% used")
        self.assertEqual(result.metrics, {"capacity_used_percent": 95.0})

    @patch("check_hadoop_modernized.CommandHealthCheck.execute_command")
    async def test_check_parsing_error(self, mock_execute):
        """Test capacity check with parsing error."""
        mock_execute.return_value = "No capacity information\n"
        result = await self.check.check()

        self.assertEqual(result.status, Status.UNKNOWN)
        self.assertEqual(result.message, "Could not determine HDFS capacity")

    @patch("check_hadoop_modernized.CommandHealthCheck.execute_command")
    async def test_check_command_error(self, mock_execute):
        """Test capacity check with command execution error."""
        mock_execute.side_effect = subprocess.SubprocessError("Command failed")
        result = await self.check.check()

        self.assertEqual(result.status, Status.UNKNOWN)
        self.assertTrue("Error checking HDFS capacity" in result.message)


class TestDataNodeStatusCheck(unittest.TestCase):
    """Test the DataNodeStatusCheck class."""

    def setUp(self):
        """Set up the test case."""
        self.check = DataNodeStatusCheck()

    def test_name_property(self):
        """Test the name property."""
        self.assertEqual(self.check.name, "datanode_status")

    @patch("check_hadoop_modernized.CommandHealthCheck.execute_command")
    async def test_check_ok_status(self, mock_execute):
        """Test datanode check with OK status."""
        mock_execute.return_value = "Live datanodes: 5\n"
        result = await self.check.check()

        self.assertEqual(result.status, Status.OK)
        self.assertEqual(result.message, "5 live DataNodes found")
        self.assertEqual(result.metrics, {"live_datanodes": 5})

    @patch("check_hadoop_modernized.CommandHealthCheck.execute_command")
    async def test_check_critical_status(self, mock_execute):
        """Test datanode check with CRITICAL status."""
        mock_execute.return_value = "Live datanodes: 0\n"
        result = await self.check.check()

        self.assertEqual(result.status, Status.CRITICAL)
        self.assertEqual(result.message, "No live DataNodes found")
        self.assertEqual(result.metrics, {"live_datanodes": 0})

    @patch("check_hadoop_modernized.CommandHealthCheck.execute_command")
    async def test_check_parsing_error(self, mock_execute):
        """Test datanode check with parsing error."""
        mock_execute.return_value = "No datanode information\n"
        result = await self.check.check()

        self.assertEqual(result.status, Status.UNKNOWN)
        self.assertEqual(result.message, "Could not determine DataNode status")

    @patch("check_hadoop_modernized.CommandHealthCheck.execute_command")
    async def test_check_command_error(self, mock_execute):
        """Test datanode check with command execution error."""
        mock_execute.side_effect = subprocess.SubprocessError("Command failed")
        result = await self.check.check()

        self.assertEqual(result.status, Status.UNKNOWN)
        self.assertTrue("Error checking DataNode status" in result.message)


class TestAPIHealthCheck(unittest.TestCase):
    """Test the APIHealthCheck class."""

    def setUp(self):
        """Set up the test case."""
        self.check = APIHealthCheck("http://example.com/api", max_update_minutes=10)

    def test_name_property(self):
        """Test the name property."""
        self.assertEqual(self.check.name, "api_health")

    def test_normalize_url(self):
        """Test URL normalization."""
        # Create test instances with different URLs to test normalization indirectly
        check1 = APIHealthCheck("example.com/api")
        check2 = APIHealthCheck("http://example.com/api")
        check3 = APIHealthCheck("https://example.com/api")
        
        self.assertEqual(check1.url, "http://example.com/api")
        self.assertEqual(check2.url, "http://example.com/api")
        self.assertEqual(check3.url, "https://example.com/api")

    @patch("httpx.AsyncClient.get")
    async def test_check_ok_status(self, mock_get):
        """Test API check with OK status."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "ok",
            "subcomponents": [
                {
                    "name": "component1",
                    "status": "ok",
                    "updated": "2025-04-11 12:00:00",
                    "message": "Running"
                },
                {
                    "name": "component2",
                    "status": "ok",
                    "updated": "2025-04-11 12:00:00",
                    "message": "Running"
                }
            ]
        }
        mock_get.return_value = mock_response

        # Mock datetime.now to return a fixed time
        with patch("check_hadoop_modernized.datetime") as mock_datetime:
            mock_datetime.strptime.return_value = asyncio.datetime(2025, 4, 11, 12, 5, 0)
            mock_datetime.now.return_value = asyncio.datetime(2025, 4, 11, 12, 5, 0)
            
            result = await self.check.check()

        self.assertEqual(result.status, Status.OK)
        self.assertTrue("All components have status \"ok\"" in result.message)
        self.assertEqual(result.metrics["components_total"], 2)
        self.assertEqual(result.metrics["components_ok"], 2)

    @patch("httpx.AsyncClient.get")
    async def test_check_warning_status_component(self, mock_get):
        """Test API check with component in warning status."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "ok",
            "subcomponents": [
                {
                    "name": "component1",
                    "status": "ok",
                    "updated": "2025-04-11 12:00:00",
                    "message": "Running"
                },
                {
                    "name": "component2",
                    "status": "error",
                    "updated": "2025-04-11 12:00:00",
                    "message": "Failed"
                }
            ]
        }
        mock_get.return_value = mock_response

        # Mock datetime.now to return a fixed time
        with patch("check_hadoop_modernized.datetime") as mock_datetime:
            mock_datetime.strptime.return_value = asyncio.datetime(2025, 4, 11, 12, 5, 0)
            mock_datetime.now.return_value = asyncio.datetime(2025, 4, 11, 12, 5, 0)
            
            result = await self.check.check()

        self.assertEqual(result.status, Status.WARNING)
        self.assertTrue("component2" in result.message)
        self.assertTrue("error" in result.message)
        self.assertEqual(result.metrics["components_total"], 2)
        self.assertEqual(result.metrics["components_ok"], 0)

    @patch("httpx.AsyncClient.get")
    async def test_check_warning_status_update_time(self, mock_get):
        """Test API check with component update time exceeding threshold."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "ok",
            "subcomponents": [
                {
                    "name": "component1",
                    "status": "ok",
                    "updated": "2025-04-11 12:00:00",
                    "message": "Running"
                },
                {
                    "name": "component2",
                    "status": "ok",
                    "updated": "2025-04-11 11:00:00",  # 1 hour old
                    "message": "Running"
                }
            ]
        }
        mock_get.return_value = mock_response

        # Mock datetime.now to return a fixed time
        with patch("check_hadoop_modernized.datetime") as mock_datetime:
            mock_datetime.strptime.side_effect = lambda date_string, format: (
                asyncio.datetime(2025, 4, 11, 12, 0, 0) if date_string == "2025-04-11 12:00:00"
                else asyncio.datetime(2025, 4, 11, 11, 0, 0)
            )
            mock_datetime.now.return_value = asyncio.datetime(2025, 4, 11, 12, 30, 0)
            
            result = await self.check.check()

        self.assertEqual(result.status, Status.WARNING)
        self.assertTrue("component2" in result.message)
        self.assertTrue("not been updated" in result.message)
        self.assertEqual(result.metrics["components_total"], 2)
        self.assertEqual(result.metrics["components_ok"], 1)

    @patch("httpx.AsyncClient.get")
    async def test_check_warning_status_main(self, mock_get):
        """Test API check with main status not OK."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "degraded",
            "subcomponents": []
        }
        mock_get.return_value = mock_response
        
        result = await self.check.check()

        self.assertEqual(result.status, Status.WARNING)
        self.assertTrue("Hadoop: degraded" in result.message)

    @patch("httpx.AsyncClient.get")
    async def test_check_http_error(self, mock_get):
        """Test API check with HTTP error."""
        mock_get.side_effect = httpx.HTTPError("Connection error")
        
        result = await self.check.check()

        self.assertEqual(result.status, Status.CRITICAL)
        self.assertTrue("Could not retrieve or parse JSON data" in result.message)


class TestHealthCheckRunner(unittest.TestCase):
    """Test the HealthCheckRunner class."""

    def setUp(self):
        """Set up the test case."""
        self.version_check = HadoopVersionCheck()
        self.health_check = HadoopHealthCommandCheck()
        self.runner = HealthCheckRunner([self.version_check, self.health_check])

    @patch.object(HadoopVersionCheck, "check")
    @patch.object(HadoopHealthCommandCheck, "check")
    async def test_run_checks_success(self, mock_health_check, mock_version_check):
        """Test running checks successfully."""
        mock_version_check.return_value = CheckResult(Status.OK, "Hadoop version: 3.3.4")
        mock_health_check.return_value = CheckResult(Status.OK, "Hadoop is healthy")
        
        results = await self.runner.run_checks()
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0][0], "hadoop_version")
        self.assertEqual(results[0][1].status, Status.OK)
        self.assertEqual(results[1][0], "hadoop_health")
        self.assertEqual(results[1][1].status, Status.OK)

    @patch.object(HadoopVersionCheck, "check")
    @patch.object(HadoopHealthCommandCheck, "check")
    async def test_run_checks_with_error(self, mock_health_check, mock_version_check):
        """Test running checks with one check failing."""
        mock_version_check.return_value = CheckResult(Status.OK, "Hadoop version: 3.3.4")
        mock_health_check.side_effect = Exception("Check failed")
        
        results = await self.runner.run_checks()
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0][0], "hadoop_version")
        self.assertEqual(results[0][1].status, Status.OK)
        self.assertEqual(results[1][0], "hadoop_health")
        self.assertEqual(results[1][1].status, Status.UNKNOWN)
        self.assertTrue("Check failed" in results[1][1].message)

    def test_get_most_severe_status(self):
        """Test getting the most severe status."""
        results = [
            ("check1", CheckResult(Status.OK, "OK")),
            ("check2", CheckResult(Status.WARNING, "Warning")),
            ("check3", CheckResult(Status.OK, "OK")),
        ]
        self.assertEqual(self.runner.get_most_severe_status(results), Status.WARNING)
        
        results = [
            ("check1", CheckResult(Status.OK, "OK")),
            ("check2", CheckResult(Status.CRITICAL, "Critical")),
            ("check3", CheckResult(Status.WARNING, "Warning")),
        ]
        self.assertEqual(self.runner.get_most_severe_status(results), Status.CRITICAL)
        
        results = [
            ("check1", CheckResult(Status.OK, "OK")),
            ("check2", CheckResult(Status.OK, "OK")),
        ]
        self.assertEqual(self.runner.get_most_severe_status(results), Status.OK)


class TestOutputFormatter(unittest.TestCase):
    """Test the OutputFormatter class."""

    def test_format_results_text(self):
        """Test formatting results as text."""
        results = [
            ("check1", CheckResult(Status.OK, "All good")),
            ("check2", CheckResult(Status.WARNING, "High usage", metrics={"usage": 85})),
        ]
        
        formatted = OutputFormatter.format_results(results, "text")
        
        self.assertTrue("[check1] OK - All good" in formatted)
        self.assertTrue("[check2] WARNING - High usage | usage=85" in formatted)

    def test_format_results_json(self):
        """Test formatting results as JSON."""
        results = [
            ("check1", CheckResult(Status.OK, "All good")),
            ("check2", CheckResult(Status.WARNING, "High usage", metrics={"usage": 85})),
        ]
        
        formatted = OutputFormatter.format_results(results, "json")
        json_data = json.loads(formatted)
        
        self.assertEqual(json_data["check1"]["status"], "OK")
        self.assertEqual(json_data["check1"]["message"], "All good")
        self.assertEqual(json_data["check2"]["status"], "WARNING")
        self.assertEqual(json_data["check2"]["message"], "High usage")
        self.assertEqual(json_data["check2"]["metrics"], {"usage": 85})


# Run the tests
if __name__ == "__main__":
    unittest.main()
