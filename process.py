import pandas as pd
import numpy as np


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
        approval_percentage[approval_type] = approval[approval_type]/total_reviews

    return approval_percentage


tweets = pd.read_csv("tweets.csv")
tweets["candidates"] = tweets.apply(get_candidates, axis=1)

counts = tweets["candidates"].value_counts()

gr = tweets.groupby("candidates").agg(get_approval)

gr["rating"] = gr["polarity"].apply(get_approval_percentages)
for candidate_rating in gr["rating"].items():
    print(candidate_rating[0], 'approve:', candidate_rating[1]
          ['approve'], 'disapprove:', candidate_rating[1]['disapprove'])
