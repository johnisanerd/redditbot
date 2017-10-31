# redditbot
# An Experiment in Karma
# Add "Nice work!" to every subreddit entry.
# Link to API information:  https://praw.readthedocs.io/en/latest/code_overview/models/subreddit.html

import re
import os
import praw
import time
import random

debug_api_on = True

def debug_api(string_in):
    if debug_api_on:
        print("Debug API: # " + string_in)

reddit = praw.Reddit('bot1', user_agent='Social_Bot_1.0')
subreddit = reddit.subreddit("RASPBERRY_PI_PROJECTS")

print("#######")
print(reddit.user.me())

# Vague replies to questions.
question_replies = [
                    "Wish I could help!  Sounds like a cool project!",
                    "Great project idea.",
                    "This is super cool. Wish I could help!",
                    "Good luck on this one!",
                    "Great project idea, I'd like to see more like this."
                    ]

project_replies = [
                    "Cool project, nice work!",
                    "This project is fabulous.",
                    "Legendary project!",
                    "Awesome project, wish I could help!",
                    "This is very useful information.  Thanks!",
                    "Great project!"
                    ]

def reply_on_project(text):
    # If it's a question, urge them along!
    if(text.find("?") > 0):
        return question_replies[random.randint(0,len(question_replies)-1)]
    # If it's a project or link, compliment the project.
    return project_replies[random.randint(0,len(project_replies)-1)]

def remove_non_ascii_1(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])

with open("posts_replied_to.txt", "r") as f:
    posts_replied_to = f.read()
    posts_replied_to = posts_replied_to.split("\n")
    posts_replied_to = list(filter(None, posts_replied_to))

print posts_replied_to

while True:
    # Get the new subreddits.
    # Check which subreddits have replies.
    # Reply to any subreddits that don't have replies.
    for submission in subreddit.new(limit=25):
        if submission.id not in posts_replied_to:
            if debug_api_on:
                print("Title: ", submission.title)
                print("Text: ", submission.selftext)
                # print("Score: ", submission.score)
                print("ID: ", submission.id)
                print("---------------------------------\n")
            # Now do this until we get a positive submission.
            not_submitted = True    # Start with it not submitted
            while not_submitted:
                try:
                    submit_text = remove_non_ascii_1(submission.selftext)
                    submit_text = reply_on_project(submit_text)
                    submission.reply(submit_text)
                    with open("posts_replied_to.txt", "a") as f:
                        f.write(submission.id + "\n")
                    # Post was submitted!  Rest for 9.5 minutes.
                    time.sleep(10)
                    not_submitted = False
                # If we get a rate limit exception, then we need to figure out how long to wait
                # and then wait that long.
                except praw.exceptions.APIException as e:
                    debug_api("Exception: " + str(e))
                    # If the error has the word "minute" in it, we just wait a number of minutes.
                    if(str(e).find("minute") > 0):
                        position = str(e).find("minutes")
                        sleep_minutes = int(filter(str.isdigit, str(e)))
                        print("Sleeping minutes: " + str(sleep_minutes))
                        time.sleep((sleep_minutes*60)+60)
                    # If the error has the word "seconds" in it, we just wait a number of seconds.
                    elif(str(e).find("seconds") > 0):
                        sleep_seconds_int = int(filter(str.isdigit, str(e)))
                        print("Sleeping seconds: " + str(sleep_seconds_int))
                        time.sleep(sleep_seconds_int)
                    else:
                        debug_api("Sleeping 10 seconds")
                        time.sleep(10)
                except Exception as e:
                    print("Unknown exception:")
                    print(str(e))
                else:
                    debug_api("Exception . . . not sure what happened.")
        else:
            print("Found a Post:  Already submitted to this one. " + str(submission.id))

    print("Checked the latest.  Sleeping for 10 minutes.")
    time.sleep(10*60)
#if __name__ == '__main__':
#    main()
