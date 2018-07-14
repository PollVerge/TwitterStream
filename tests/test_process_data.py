#!/usr/bin/python3
import pytest
import process_data


@pytest.mark.parametrize("test_input, expected", [
    ({'text': 'This tweet contains the name Trump'}, 'trump'),
    ({'text': 'This tweet contains the name Trump and Clinton'}, None),
    ({'text': 'This tweet contains the name Drump and Blinton'}, None),
])
def test_get_candidates(test_input, expected):
    assert process_data.get_candidates(test_input) == expected
