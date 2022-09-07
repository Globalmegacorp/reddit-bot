#!/usr/bin/env python3
import praw
import config
import time
import os
import requests
import datetime
import pprint

r = praw.Reddit(username = config.username,
		password = config.password,
		client_id = config.client_id,
		client_secret = config.client_secret,
		user_agent = ("GlobalMegaBot v1.0"))

DEBUG=False

def log(message):
    ts = str(datetime.datetime.now())

    if (DEBUG):
        print(ts +" " + message)

    with open (config.debuglog, "a") as f:
                f.write(ts + " " + message + "\n")


def check_comments(r, subreddit):
        for comment in r.subreddit(subreddit).comments(limit=config.low_score_comment_lookback):
            if (comment.score <= config.low_score_notify_threshold and comment.banned_by == None and comment.id not in comments_acted):
                log ("Acting on " + comment.id)
                message = "Comment with score: " + str(comment.score) + "\n" + comment.body[:200] + "\n" + "https://reddit.com" + comment.permalink
                #pprint.pprint(vars(comment))
                log (message)
                notify_discord(message)
                mark_comment_acted(comment.id)

def check_mod_queue(r):
    now = (int(time.time()))
    modqueue = r.subreddit("mod").mod.modqueue(limit=None)
    count = len(list(modqueue))
    if (count > 0 and now-modqueue_last_notify > config.reports_notify_pause_seconds):
        message = "There are currently **" + str(count) + "** items in the modqueue.\nhttps://www.reddit.com/r/" + config.subreddit + "/about/modqueue/"
        log(message)
        notify_discord(message)
        return now
    else:
        return modqueue_last_notify

def check_unmodded(r):
    now = (int(time.time()))
    unmodded_posts = 0
    for post in r.subreddit("mod").mod.unmoderated():
        if (now-(int(post.created)) > config.max_unmodded_age):
            unmodded_posts+=1

    if (unmodded_posts > 0 and now-unmod_last_notify > config.unmodded_notify_pause_seconds):
        message = "There are currently **" + str(unmodded_posts) + "** unmoderated posts.\nhttps://www.reddit.com/r/" + config.subreddit + "/about/unmoderated/"
        log(message)
        notify_discord(message)
        return now
    else:
        return unmod_last_notify

def notify_discord(message):
    if (DEBUG):
        return

    data = {
            "content" : message
    }

    result = requests.post(config.discord_webhook, json = data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        log(err)
    else:
        log("Payload delivered successfully, code {}.".format(result.status_code))

def mark_comment_acted(comment_id):
    comments_acted.append(comment_id)
    with open (config.commentdb, "a") as f:
        f.write(comment_id + "\n")

def get_acted_comments():
    if not os.path.isfile(config.commentdb):
        comments_acted = []
    else:
        with open(config.commentdb, "r") as f:
            comments_acted = f.read()
            comments_acted = comments_acted.split("\n")

    return comments_acted

comments_acted = get_acted_comments()
modqueue_last_notify = 0
unmod_last_notify = 0

while True:
    log ("Starting a run")
    check_comments(r, config.subreddit)
    modqueue_last_notify = check_mod_queue(r)
    unmod_last_notify = check_unmodded(r)
    log ("Run complete. Sleeping " + str(config.bot_sleep_seconds/60) + " minutes")
    time.sleep(config.bot_sleep_seconds)
