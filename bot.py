import tweepy
import schedule
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Load credentials
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

# Authenticate
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Example tweet list for one project (INFINT)
tweets = [
    "How AI is transforming DeFi: INFINT leads the way.",
    "Discover seamless on-chain experiences with INFINT.",
    "The future of decentralized finance is intelligent. #INFINT"
]

# Function to post a tweet
def post_tweet():
    tweet = tweets.pop(0)
    api.update_status(tweet)
    print(f"Tweeted: {tweet}")
    tweets.append(tweet)  # rotate tweets

# Schedule tweets every 30 minutes
schedule.every(30).minutes.do(post_tweet)

print("Bot started...")

# Main loop
while True:
    schedule.run_pending()
    time.sleep(10)
  
