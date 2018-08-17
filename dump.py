#!/usr/bin/python3

import settings
import pymongo
import datetime


client = pymongo.MongoClient(settings.CONNECTION_STRING)
db = client.candidate

rollup_time = datetime.datetime.utcnow()


def rollup_raw_data():
    raw_coll = getattr(db, settings.RAW_COLLECTION_NAME)
    rollup_coll = getattr(db, settings.ROLLUP_COLLECTION_NAME)

    rollup_coll.insert_many(raw_coll.find({'created': {'$lt': rollup_time}}))
    raw_coll.delete_many({'created': {'$lt': rollup_time}})


def main():
    rollup_raw_data()


if __name__ == '__main__':
    main()
