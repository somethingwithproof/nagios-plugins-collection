import pytest
from check_mounts import transform_ssh_result_into_list_of_dicts

def test_transform_ssh_result_into_list_of_dicts():
    source_result = [
        ['dev1', '/mnt1', 'type1', 'rw', '1', '2'],
        ['dev2', '/mnt2', 'type2', 'ro', '3', '4'],
        ['dev3', '/mnt3', 'type3', 'rw', '5', '6']
    ]

    expected_result = [
        {
            'device': 'dev1',
            'mountpoint': '/mnt1',
            'type': 'type1',
            'opts': 'rw',
            'n1': '1',
            'n2': '2'
        },
        {
            'device': 'dev2',
            'mountpoint': '/mnt2',
            'type': 'type2',
            'opts': 'ro',
            'n1': '3',
            'n2': '4'
        },
        {
            'device': 'dev3',
            'mountpoint': '/mnt3',
            'type': 'type3',
            'opts': 'rw',
            'n1': '5',
            'n2': '6'
        }
    ]

    result = transform_ssh_result_into_list_of_dicts(source_result)
    assert result == expected_result
