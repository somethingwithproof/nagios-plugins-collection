import pytest
from membase_stats import MembaseStats

def test_before_work():
    # Create an instance of MembaseStats
    stats = MembaseStats()

    # Test with existing data file
    stats.data_file_name = "existing_file.txt"
    stats.before_work()
    assert stats.prev_stats  # Assert that prev_stats is populated

    # Test with non-existing data file
    stats.data_file_name = "non_existing_file.txt"
    stats.before_work()
    assert stats.prev_stats == set()  # Assert that prev_stats is empty

def test_after_work(tmp_path):
    # Create an instance of MembaseStats
    stats = MembaseStats()

    # Set a temporary directory as the data file location
    stats.data_file_name = str(tmp_path / "data_file.txt")

    # Test writing to the data file
    stats.prev_stats = {"item1": 10, "item2": 20}
    stats.after_work()
    assert stats.prev_stats == {"item1": 10, "item2": 20}  # Assert that prev_stats remains unchanged

    # Read the data file and verify its content
    with open(stats.data_file_name) as file:
        content = file.read()
    assert content == "item1 10\nitem2 20\n"  # Assert that the content is correct

def test_get_status_with_valid_url():
    # Create an instance of MembaseStats
    stats = MembaseStats()

    # Set the URL, username, and password
    stats.url = "http://example.com"
    stats.username = "user"
    stats.password = "pass"

    # Mock the urllib.request.urlopen function to return sample content
    class MockResponse:
        def read(self):
            return b'{"op": {"samples": {"curr_items": [10]}}}'

    def mock_urlopen(request):
        return MockResponse()

    stats.get_status(src_url=stats.url, remote_user=stats.username, remote_pass=stats.password, urlopen=mock_urlopen)

    # Assert that the d_stats attribute is populated with data
    assert stats.d_stats == {"curr_items": 10}

def test_get_status_with_missing_url(capfd):
    # Create an instance of MembaseStats
    stats = MembaseStats()

    # Set the URL to None
    stats.url = None

    # Call the get_status method
    stats.get_status(src_url=stats.url, remote_user="user", remote_pass="pass")

    # Capture the printed output
    captured = capfd.readouterr()

    # Assert the error message and script exit
    assert "Error: Missing source URL" in captured.out
    assert captured.err == ""
    assert stats.d_stats == {}

def test_process_data():
    # Create an instance of MembaseStats
    stats = MembaseStats()

    # Test process_data with a valid key
    stats.d_stats = {"curr_items": 10}
    result = stats.process_data("curr_items")
    assert result == "current_active_items=10 "

    # Test process_data with an unknown key
    stats.d_stats = {"unknown_key": 20}
    result = stats.process_data("unknown_key")
    assert result == "unknown_key=20 "

def test_get_resident_ratio():
    # Create an instance of MembaseStats
    stats = MembaseStats()

    # Test get_resident_ratio with valid data
    stats.d_stats = {"ep_num_active_non_resident": 5, "curr_items": 20}
    result = stats.get_resident_ratio()
    assert result == "resident_item_ratio=75% "

    # Test get_resident_ratio with invalid data
    stats.d_stats = {"ep_num_active_non_resident": 0, "curr_items": 0}
    result = stats.get_resident_ratio()
    assert result == ""

def test_get_cache_miss_ratio():
    # Create an instance of MembaseStats
    stats = MembaseStats()

    # Test get_cache_miss_ratio with valid data
    stats.d_stats = {"get_hits": 100, "ep_bg_fetched": 10}
    result = stats.get_cache_miss_ratio()
    assert result == "cache_miss_ratio=10% "

    # Test get_cache_miss_ratio with invalid data
    stats.d_stats = {"get_hits": 0, "ep_bg_fetched": 0}
    result = stats.get_cache_miss_ratio()
    assert result == ""

def test_get_replica_resident_ratio():
    # Create an instance of MembaseStats
    stats = MembaseStats()

    # Test get_replica_resident_ratio with valid data
    stats.d_stats = {"ep_num_non_resident": 10, "curr_items_tot": 30, "curr_items": 20, "ep_num_active_non_resident": 5}
    result = stats.get_replica_resident_ratio()
    assert result == "replica_resident_ratio=66.66666666666666% "

    # Test get_replica_resident_ratio with invalid data
    stats.d_stats = {"ep_num_non_resident": 0, "curr_items_tot": 0, "curr_items": 0, "ep_num_active_non_resident": 0}
    result = stats.get_replica_resident_ratio()
    assert result == ""

def test_main(capfd):
    # Create an instance of MembaseStats
    stats = MembaseStats()

    # Mock the get_status method to avoid making actual requests
    stats.get_status = lambda src_url, remote_user, remote_pass: None

    # Test main method with valid arguments
    stats.url = "http://example.com"
    stats.username = "user"
    stats.password = "pass"
    stats.list_stats = True
    stats.main()

    # Capture the printed output
    captured = capfd.readouterr()

    # Assert the output
    assert "curr_items" in captured.out
    assert captured.err == ""

def test_main_missing_url(capfd):
    # Create an instance of MembaseStats
    stats = MembaseStats()

    # Test main method with missing URL
    stats.url = None
    stats.main()

    # Capture the printed output
    captured = capfd.readouterr()

    # Assert the error message and script exit
    assert "Error: Missing source URL" in captured.out
    assert captured.err == ""

def test_main_coverage(capfd):
    # Create an instance of MembaseStats
    stats = MembaseStats()

    # Mock the get_status method to avoid making actual requests
    stats.get_status = lambda src_url, remote_user, remote_pass: None

    # Test main method with all paths covered
    stats.url = "http://example.com"
    stats.username = "user"
    stats.password = "pass"
    stats.main()
    stats.list_stats = True
    stats.main()
    stats.list_stats = False
    stats.main(args=["all"])
    stats.main(args=["metric1", "metric2"])

    # Capture the printed output
    captured = capfd.readouterr()

    # Assert the output
    assert captured.err == ""

# Run the tests
pytest.main(["-v", "--cov=membase_stats", "--cov-report=html"])
