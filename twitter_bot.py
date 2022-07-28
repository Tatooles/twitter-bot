import tweepy

#bearer_token = 'AAAAAAAAAAAAAAAAAAAAAHTmXgEAAAAAUNuZWKqsMgfmv4LWXlzkIQQ9X7A%3DzWWjCD4BqF7vao3fswhdpa3G3wMkJH1Jk5AOYPqxbuBuADomcg'
consumerKey = 'IODvXnxsaiG8cU7MtY4XZhyLN'
consumerSecret = 'R9uqkxEXxQdmYFxFwdOSIqibi17WLqDH45QDAC337uC6lYcRWQ'

accessToken = '1478092305361952769-SbteiPfJvqvCxQqzdBy76bycKf8eMd'
accessToken_secret = 'lFwfVInbbgJOQ1gmgMmr7U7jHn7ZLygTTcPGrRXJhPg5G'

client = tweepy.Client(consumer_key=consumerKey, consumer_secret=consumerSecret, access_token=accessToken, access_token_secret=accessToken_secret)

## Idea: maybe use a hashtag to control what the bot will return
## Better than a different type of string because that could randomly be part of the tweet
## Random string would probably work though

FILE_NAME = 'last_seen_id.txt'

def storeId(last_seen_id, filename):
    with open(filename, 'w') as file:
        file.write(str(last_seen_id))

def retrieveId(filename):
    with open(filename, 'r') as file:
        id = int(file.read().strip())
    return id

lastId = retrieveId(FILE_NAME)
response = client.get_users_mentions(id=1478092305361952769, since_id=lastId, expansions=['author_id'], user_auth=True)
tweets = response.data

# users = {user['id'] : user for user in users}
if tweets:
    for tweet in reversed(tweets):
        lastId = tweet.id
        storeId(lastId, FILE_NAME)
        tokens = tweet.text.lower().split()
        if tokens[1] == 'echo':
            print("echoing")
            # Echo their tweet
            client.create_tweet(text=tweet.text, in_reply_to_tweet_id=tweet.id)