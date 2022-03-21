#!/usr/bin/python3

import pytest
import sys
from mock import patch
import subprocess

sys.path.insert(0, '../TwitterStream')

import restarter


def mock_getoutput(*args, **kwargs):
    return ['process_one', 'process_two', 'process_three']


@patch.multiple(subprocess, getoutput=mock_getoutput)
def test_restarter_main_restart():
    restarter.main('process_one')


@patch.multiple(subprocess, getoutput=mock_getoutput)
def test_restarter_main_no_restart():
    restarter.main('process_zero')
