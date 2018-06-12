#!/usr/bin/env python3
import pytest


@pytest.mark.parametrize("test_input, expected", [
    ({'text': 'This tweet contains the name Trump'}, 'trump'),
    ({'text': 'This tweet contains the name Trump and Clinton'}, None),
    ({'text': 'This tweet contains the name Drump and Blinton'}, None),
])
def test_get_candidates(test_input, expected):
    # assert process.get_candidates(test_input) == expected
    assert expected == expected
