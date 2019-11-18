import tweepy
import time

# change arguments with personal API info !!!
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# avoid to break program because of twitter rate limit for API calls
def limit_handler(cursor):
    try:
        while True:
            yield cursor.next()
    except tweepy.RateLimitError:
        time.sleep(300)
    except StopIteration:
        return

# follow back all users who follow you with more than 1000 followers
def follow_back():
    for follower in limit_handler(tweepy.Cursor(api.followers).items()):
        try:
            if(follower.followers_count > 1000):
                follower.follow()
        except StopIteration:
            return

# likes a certain amount of tweets containing a keyword
def like_tweet_with_keyword(keyWord, n_of_tweets):
    for tweet in limit_handler(tweepy.Cursor(api.search, keyWord).items(n_of_tweets)):
        try:
            tweet.favorite()
            print('Tweets liked')
        except tweepy.TweepError as err:
            print(err.reason)
        except StopIteration:
            break

like_tweet_with_keyword('Software Engineering', 1)
follow_back()