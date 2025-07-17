# BMSK-X-BOT: Automated Twitter Curator Bot

import os
import random
import time
import schedule
import openai
import tweepy
from datetime import datetime
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()

# --- Twitter API Setup ---
api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_SECRET")

auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
twitter = tweepy.API(auth)

# --- OpenAI API Setup ---
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Projects and Configuration ---
projects = {
    "YEET": {"hashtag": "#YEET", "topics": ["memecoin utility", "culture", "on-chain trends"]},
    "LOMBARD": {"hashtag": "#LOMBARD", "topics": ["real yield", "BTC yield", "defi risk"]},
    "NEAR": {"hashtag": "#NEAR", "topics": ["chain abstraction", "open web", "developer UX"]},
    "INFINT": {"hashtag": "#INFINT", "topics": ["AI x DeFi", "intelligent protocols", "automated liquidity"]}
}

# Rotate projects daily based on weekday
project_keys = list(projects.keys())
def get_today_project():
    return project_keys[datetime.now().weekday() % len(project_keys)]

# --- Generate a tweet ---
def generate_tweet(project):
    topic = random.choice(projects[project]['topics'])
    hashtag = projects[project]['hashtag']
    prompt = f"Write a professional, curated, educative tweet about {topic} in the {project} project. Use a smart tone and include {hashtag}. Limit to 270 characters."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    tweet = response.choices[0].message.content.strip()
    return tweet

# --- Tweet Posting Logic ---
def post_tweet():
    project = get_today_project()
    tweet = generate_tweet(project)
    try:
        twitter.update_status(tweet)
        print(f"Posted for {project}: {tweet}")
    except Exception as e:
        print(f"Error posting tweet: {e}")

# --- Schedule 100 tweets/day ---
def schedule_tweets():
    for i in range(100):
        schedule.every(12).minutes.do(post_tweet)

# --- Run Scheduler ---
if __name__ == "__main__":
    print("BMSK-X-BOT started...")
    schedule_tweets()
    while True:
        schedule.run_pending()
        time.sleep(1)

