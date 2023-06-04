import pytest
from unittest.mock import MagicMock
from myscript import VerticaConnector


@pytest.fixture
def mock_connection():
    # Mock the psycopg2 connection object
    connection = MagicMock()
    cursor = connection.cursor.return_value
    cursor.fetchone.return_value = (10,)  # Sample result value

    # Patch the connect method to return the mocked connection
    with patch('myscript.psycopg2.connect', return_value=connection):
        yield connection


def test_execute_queries(mock_connection):
    connector = VerticaConnector('localhost', 'user', 'password', 'database')
    queries = ['SELECT COUNT(*) FROM table1;', 'SELECT COUNT(*) FROM table2;']

    results = connector.execute_queries(queries)

    assert len(results) == 2
    assert results == [10, 10]  # Sample expected results


def test_print_results(capsys):
    connector = VerticaConnector('localhost', 'user', 'password', 'database')
    results = [10, 20, 30]

    connector.print_results(results)

    captured = capsys.readouterr()
    assert captured.out.strip() == 'R1: 10\nR2: 20\nR3: 30'


if __name__ == '__main__':
    pytest.main()
