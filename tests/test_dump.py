#!/usr/bin/python3

import pytest
import sys
from mock import patch

sys.path.insert(0, '../TwitterStream')

import dump


class mock_mongo_collection:
    def find(self, *args, **kwargs):
        pass

    def insert_many(self, *args, **kwargs):
        pass

    def delete_many(self, *args, **kwargs):
        pass


class mock_mongo_database:
    test_raw_coll = mock_mongo_collection()
    test_roll_coll = mock_mongo_collection()


def test_rollup_raw_data():
    dump.rollup_raw_data(
        db=mock_mongo_database, raw_collection='test_raw_coll', rollup_collection='test_roll_coll')


def mock_rollup_raw_data(*args, **kwargs):
    pass


@patch.object(dump, 'rollup_raw_data', mock_rollup_raw_data)
def test_rollup_raw_data_main():
    dump.main()
