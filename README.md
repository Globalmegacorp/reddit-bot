# reddit-bot
## Overview
This is a bot, written in python, for helping moderators out on a subreddit.

You will need:

- Somewhere to run it. Tested on Ubuntu 18 with Python 3.
- The [PRAW](https://praw.readthedocs.io/en/stable/) library
- A reddit account for the bot to run under. Highly recommended you create a dedicated account and not your own.
- A subreddit you're a mod on. The user account you're using will also need to be a mod.
- A discord where notifications can be sent. Google around for how to create a discord webhook.

## Functionality

This bot does a few things:

- Notification on comments with a low score
- Notification of tasks in the modqueue (reports, typically)
- Notification of unmoderated posts. In the subs I look after, we review all incoming posts. This functionality alerts us to posts which have sat unmoderated for 4 hours (by default)

# Setup
Make a copy of config.py.tmpl as config.py and edit the values. You will need an account and client_id and client_secret. Google around for instructions. It's not complicated.
Simply run as ./reddit_bot.py in a screen.

## Config

| Config Name | Description |
| ----------- | ----------- |
| subreddit | | Your subreddit here |
| commentdb | File to store which comments have already triggered a notification |
| discord_webhook | Webhook for posting notifications |
| reports_notify_pause_seconds | Pause between notifying about reports, default 30 minutes |
| unmodded_notify_pause_seconds | Pause between notifying about unmodded posts, default 1 hour |
| max_unmodded_age | Max age of an unmodded post before notifying, default 4 hours |
| bot_sleep_seconds | Sleep between runs, default 10 minutes |
| low_score_comment_lookback | How many comments to look back at, default 500. Might need to be higher on a busy sub |
| low_score_notify_threshold | What score to notify negative comments on, default -10 |
