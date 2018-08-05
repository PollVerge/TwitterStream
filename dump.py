#!/usr/bin/python3

import settings
import pymongo
import datetime


client = pymongo.MongoClient(settings.CONNECTION_STRING)
db = client.candidate

rollup_time = datetime.datetime.utcnow()


def rollup_raw_data():
    raw_coll = getattr(db, settings.RAW_TABLE_NAME)
    rollup_coll = getattr(db, settings.ROLLUP_TABLE_NAME)

    for doc in raw_coll.find({'created': {'$lt': rollup_time}}):
        rollup_coll.insert_one(doc)

    raw_coll.delete_many({'created': {'$lt': rollup_time}})


def main():
    rollup_raw_data()


if __name__ == '__main__':
    main()
