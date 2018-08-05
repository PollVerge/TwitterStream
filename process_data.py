#!/usr/bin/python3

import pandas as pd
import numpy as np
import pymongo
import datetime
import settings

client = pymongo.MongoClient(settings.CONNECTION_STRING)
db = client.candidate

rollup_time = datetime.datetime.utcnow()


def get_candidates(row):
    candidates = []
    text = row["text"].lower()
    if "clinton" in text or "hillary" in text:
        candidates.append("clinton")
    if "trump" in text or "donald" in text:
        candidates.append("trump")
    if "sanders" in text or "bernie" in text:
        candidates.append("sanders")
    if not candidates:
        return None
    elif len(candidates) > 1:
        return None
    return candidates[0]


def get_approval(column):
    results = {
        'approve': 0,
        'neutral': 0,
        'disapprove': 0,
    }
    for row in column:
        if row > 0.01:
            results['approve'] += 1
        if 0.01 >= row and row >= -0.01:
            results['neutral'] += 1
        else:
            results['disapprove'] += 1
    return results


def get_approval_percentages(approval):
    total_reviews = sum(approval.values())
    approval_percentage = {
        'approve': 0,
        'neutral': 0,
        'disapprove': 0,
    }
    for approval_type in approval:
        approval_percentage[approval_type] = approval[approval_type] / total_reviews

    return approval_percentage


def add_ratings_to_mongo(ratings, counts):
    table = db[settings.PROCESSED_TABLE_NAME]

    for candidate_rating in ratings.items():
        try:
            record = {
                'candidate': candidate_rating[0],
                'created_at': rollup_time,
                'count': int(getattr(counts, candidate_rating[0], None))
            }
            record.update(candidate_rating[1])
            table.insert_one(record)
        except pymongo.errors.PyMongoError as err:
            print(err)


def main():
    rollup_coll = getattr(db, settings.ROLLUP_TABLE_NAME)
    tweets = pd.DataFrame(
        list(rollup_coll.find({'created': {'$lt': rollup_time}}))
    )

    tweets["candidates"] = tweets.apply(get_candidates, axis=1)

    counts = tweets["candidates"].value_counts()

    gr = tweets.groupby("candidates").agg(get_approval)

    gr["rating"] = gr["polarity"].apply(get_approval_percentages)

    add_ratings_to_mongo(ratings=gr["rating"], counts=counts)
    rollup_coll.delete_many({'created': {'$lt': rollup_time}})


if __name__ == '__main__':
    main()
