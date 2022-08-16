import tweepy
import gspread
import sys

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

# This function takes in a request string from the user, and returns what the bot will respond with
def return_stats(request_string):
    # String format @sports_guesses SPORT PLAYER_FIRSTNAME PLAYER_LASTNAME STAT YEAR
    # Example: @sports_guesses NBA Lebron James ppg 2021-22
    tokens = request_string.split()
    if(tokens[1] != 'NBA'):
        return 'ERROR - I could not process your request. Reason: Invalid sport. Please request a valid sport. Currently supported sports: NBA'
    return ''

lastId = retrieveId()
response = client.get_users_mentions(id=1478092305361952769, since_id=lastId, expansions=['author_id'], user_auth=True)
tweets = response.data
if tweets:
    for tweet in reversed(tweets):
        lastId = tweet.id
        storeId(lastId)
        tweet_text = return_stats(tweet.text.lower())
        client.create_tweet(text=tweet_text, in_reply_to_tweet_id=tweet.id)

if __name__ == '__main__':
    print(return_stats(sys.argv[1]))