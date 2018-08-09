#!/usr/bin/python3

import pandas as pd
import numpy as np
import pymongo
import datetime
import settings

client = pymongo.MongoClient(settings.CONNECTION_STRING)
db = client.candidate

rollup_time = datetime.datetime.utcnow()


def get_candidates(row, candidate_tracker):
    candidates = {}
    text = row['text'].lower()

    for candidate in candidate_tracker:
        for term in candidate['track_terms']:
            if term in text:
                candidates[candidate['keyword']] = 1

    if len(candidates) == 0:
        return None
    return tuple(candidates.keys())


def get_approval(column):
    results = {
        'approve': 0,
        'neutral': 0,
        'disapprove': 0,
        'count': 0,
    }

    for row in column:
        if row is not None:
            if row > 0:
                results['approve'] += 1
            elif row == 0:
                results['neutral'] += 1
            else:
                results['disapprove'] += 1
            results['count'] += 1
    return results


def get_approval_percentages(approval):
    approval_percentage = {
        'approve': 0,
        'neutral': 0,
        'disapprove': 0,
    }
    for approval_type in approval:
        approval_percentage[approval_type] = approval[approval_type] / approval['count']

    return approval_percentage


def add_ratings_to_mongo(polarity):
    collection = getattr(db, settings.PROCESSED_COLLECTION_NAME)

    records = {}
    for (candidates, candidate_rating) in polarity.items():
        for candidate in candidates:
            if candidate in records:
                for (key, value) in candidate_rating.items():
                    records[candidate][key] += value
            else:
                record = {
                    'candidate': candidate,
                    'created_at': rollup_time,
                }
                record.update(candidate_rating)
                records[candidate] = record

    try:
        collection.insert_many(list(records.values()))
    except pymongo.errors.PyMongoError as err:
        print(err)


def main():
    rollup_coll = getattr(db, settings.ROLLUP_COLLECTION_NAME)
    tweets = pd.DataFrame(list(rollup_coll.find({'created': {'$lt': rollup_time}})))

    candidates = []

    collection = getattr(db, settings.TRACK_COLLECTION_NAME)
    for candidate in collection.find():
        candidates.append(candidate)

    tweets['candidate'] = tweets.apply(get_candidates, axis=1, candidate_tracker=candidates)
    gr = tweets.groupby('candidate').agg({'polarity': get_approval})

    add_ratings_to_mongo(polarity=gr['polarity'])
    rollup_coll.delete_many({'created': {'$lt': rollup_time}})


if __name__ == '__main__':
    main()
