import pytest
import pdb
from demo import find_min, helper

@pytest.mark.parametrize(
    "arr, expected",
    [ 
        ([2, 3, 10], 2),
        ([1001, 2000, 5298, 1209], 1001),
        ([], None)
    ]
)

def test_find_min(arr, expected):
    assert find_min(arr) == expected

def test_find_min_error(capsys):
    find_min(None)
    out, err = capsys.readouterr()
    assert err == 'fatal error: input array should not be none\n'

def test_helper(capsys):
    helper()
    out, err = capsys.readouterr()
    assert out == 'find_min(arr): function to find minimum number in array\n'