import os
import psycopg2
import main

def test_main():
    os.environ['VERTICA_HOST'] = 'test_host'
    os.environ['VERTICA_USER'] = 'test_user'
    os.environ['VERTICA_PASSWORD'] = 'test_password'
    with mock.patch('psycopg2.connect') as mock_connect:
        mock_cursor = mock.MagicMock()
        mock_connect.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        main.main()
        # Assert that the queries were executed
        mock_cursor.execute.assert_has_calls([
            mock.call("select count(*) from nodes where node_state = 'DOWN';"),
            mock.call("select count(*) from active_events where event_code_description = 'Too Many ROS Containers';"),
            mock.call("select count(*) from active_events where event_code_description = 'Recovery Failure';"),
            mock.call("select count(*) from active_events where event_code_description = 'Stale Checkpoint';")
