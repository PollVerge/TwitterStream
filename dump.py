#!/usr/bin/python3

import settings
from bson.json_util import dumps
import pymongo


def main():
    client = pymongo.MongoClient(settings.CONNECTION_STRING)
    db = client.candidate
    collection = getattr(db, settings.RAW_TABLE_NAME)
    cursor = collection.find()

    with open(settings.JSON_NAME, 'w') as jsonfile:
        jsonfile.write(dumps(cursor))


if __name__ == '__main__':
    main()
