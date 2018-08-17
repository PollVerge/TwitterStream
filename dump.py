#!/usr/bin/python3

import settings
import pymongo
import datetime


client = pymongo.MongoClient(settings.CONNECTION_STRING)
database = client.candidate

rollup_time = datetime.datetime.utcnow()


def rollup_raw_data(db, raw_collection, rollup_collection):
    raw_coll = getattr(db, raw_collection)
    rollup_coll = getattr(db, rollup_collection)

    rollup_coll.insert_many(raw_coll.find({'created': {'$lt': rollup_time}}))
    raw_coll.delete_many({'created': {'$lt': rollup_time}})


def main():
    rollup_raw_data(db=database, raw_collection=settings.RAW_COLLECTION_NAME,
                    rollup_collection=settings.ROLLUP_COLLECTION_NAME)


if __name__ == '__main__':
    main()
