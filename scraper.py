#!/usr/bin/python3

import settings
import tweepy
import pymongo
from textblob import TextBlob
import json

client = pymongo.MongoClient(settings.CONNECTION_STRING)
db = client.candidate


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if hasattr(status, 'retweeted_status'):
            try:
                text = status.retweeted_status.extended_tweet['full_text']
            except AttributeError:
                text = status.retweeted_status.text
        else:
            try:
                text = status.extended_tweet['full_text']
            except AttributeError:
                text = status.text
        description = status.user.description
        loc = status.user.location
        coords = status.coordinates
        try:
            place = status.place
        except AttributeError:
            place = None
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        bg_color = status.user.profile_background_color
        blob = TextBlob(text)
        sent = blob.sentiment

        if coords is not None:
            coords = json.dumps(coords)

        if place is not None:
            place = json.dumps({
                'full_name': place.full_name,
                'country_code': place.country_code,
            })

        collection = db[settings.RAW_COLLECTION_NAME]
        try:
            collection.insert_one(dict(
                user_description=description,
                user_location=loc,
                coordinates=coords,
                text=text,
                place=place,
                user_name=name,
                user_created=user_created,
                user_followers=followers,
                id_str=id_str,
                created=created,
                retweet_count=retweets,
                user_bg_color=bg_color,
                polarity=sent.polarity,
                subjectivity=sent.subjectivity,
            ))
        except pymongo.errors.PyMongoError as err:
            print(err)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False


def main():
    auth = tweepy.OAuthHandler(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
    auth.set_access_token(settings.TWITTER_KEY, settings.TWITTER_SECRET)
    api = tweepy.API(auth)

    track_terms = []
    collection = db[settings.TRACK_COLLECTION_NAME]
    for record in collection.find():
        terms = record['track_terms']
        track_terms = track_terms + terms

    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener, tweet_mode='extended')
    stream.filter(track=track_terms)


if __name__ == '__main__':
    main()
