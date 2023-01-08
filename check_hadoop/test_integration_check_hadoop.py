
import subprocess

def test_integration():
    # Test with valid URL that returns valid JSON data with component statuses "ok"
    result = subprocess.run(["python", "hadoop.py", "-url=http://somewhere.us/api/component/hadoop"], capture_output=True)
    assert result.returncode == 0
    assert "OK - mem:" in result.stdout.decode()
    
    # Test with valid URL that returns valid JSON data with component statuses "warning"
    result = subprocess.run(["python", "hadoop.py", "-url=http://somewhere.us/api/component/hadoop?status=warning"], capture_output=True)
    assert result.returncode == 1
    assert "WARNING - component" in result.stderr.decode()
    
    # Test with valid URL that returns valid JSON data with component statuses "critical"
    result = subprocess.run(["python", "hadoop.py", "-url=http://somewhere.us/api/component/hadoop?status=critical"], capture_output=True)
    assert result.returncode == 2
    assert "CRITICAL - component" in result.stderr.decode()
    
    # Test with valid URL that returns valid JSON data with component statuses "ok" and time since last update within acceptable range
    result = subprocess.run(["python", "hadoop.py", "-url=http://somewhere.us/api/component/hadoop", "-t=60"], capture_output=True)
    assert result
