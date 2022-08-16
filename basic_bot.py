import tweepy
import gspread

gc = gspread.service_account('credentials.json')

# Open a sheet from a spreadsheet in one go
wks = gc.open("last-tweet-id").sheet1

consumerKey = 'IODvXnxsaiG8cU7MtY4XZhyLN'
consumerSecret = 'R9uqkxEXxQdmYFxFwdOSIqibi17WLqDH45QDAC337uC6lYcRWQ'

accessToken = '1478092305361952769-SbteiPfJvqvCxQqzdBy76bycKf8eMd'
accessToken_secret = 'lFwfVInbbgJOQ1gmgMmr7U7jHn7ZLygTTcPGrRXJhPg5G'

client = tweepy.Client(consumer_key=consumerKey, consumer_secret=consumerSecret, access_token=accessToken, access_token_secret=accessToken_secret)

def storeId(last_seen_id):
    wks.update('A2', str(last_seen_id))

def retrieveId():
    return int(wks.acell('A2').value)

lastId = retrieveId()
response = client.get_users_mentions(id=1478092305361952769, since_id=lastId, expansions=['author_id'], user_auth=True)
tweets = response.data
if tweets:
    for tweet in reversed(tweets):
        lastId = tweet.id
        storeId(lastId)
        tokens = tweet.text.lower().split()
        if tokens[1] == 'echo':
            # Echo their tweet
            client.create_tweet(text=tweet.text, in_reply_to_tweet_id=tweet.id)