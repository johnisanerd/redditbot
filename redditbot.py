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

reddit = praw.Reddit('bot1', user_agent='Happiness_Project_1.0')

posts_replied_to = []

print("#######")
print("Reddit User: " + str(reddit.user.me()))



# Vague replies to questions.
question_replies = [
                    "Wish I could help!  Sounds like a cool project!",
                    "Great project idea.",
                    "This is super cool. Wish I had time to help!",
                    "Wish I had more free time to make things like this.",
                    "Awesome project, wish I could help!",
                    "Good luck on this one!",
                    "Great project idea, I'd like to see more like this."
                    ]

project_replies = [
                    "Cool project, nice work!",
                    "Mad high fives!",
                    "This project is fabulous.",
                    "Legendary project!",
                    "Pretty useful information.  Thanks!",
                    "Fabulous!",
                    "Very cool!  Keep up the good work!",
                    "Nice description.",
                    "Supercool",
                    "bangin project mate!!",
                    "Great project!"
                    ]

compliments_pictures = [
                "Nice picture indeed!",
                "Beautiful!",
                "Looks great!",
                "Fantastic!",
                "Awesome picture bro!",
                "Good one!",
                "Nice pic!",
                "Nice picture!  Love the details!",
                "Made my day.",
                "Just perfect!",
                "Magnificent!",
                "Extremely beautiful . . . .",
                "Elaborate",
                "Impressive!",
                "A dramatic landscape of magnificent!"
                "Splendid",
                "spectacular",
                "impressive",
                "striking",
                "glorious",
                "superb",
                "majestic",
                "Awesome!",
                "Inspiring",
                "breathtaking",
                "Sumptuous",
                "Resplendent",
                "Grand",
                "Impressive",
                "Imposing",
                "Monumental",
                "Palatial",
                "Noble",
                "Stately",
                "Exalted",
                "Royal",
                "Regal!",
                "Imperial!",
                "Princely",
                "Opulent",
                "Fine looking!",
                "Luxurious",
                "Lavish",
                "Rich!",
                "Brilliant!",
                "Radiant!",
                "Dazzling!",
                "Beautiful!",
                "Elegant!",
                "Gorgeous!",
                "Elevated!",
                "Transcendent!",
                "Informalsplendiferous!",
                "Ritzy!",
                "Posh!",
                "Raresplendacious!",
                "Magnolious!",
                "Cool, nice work!",
                "Mad high fives!",
                "This project is fabulous.",
                "Legendary pic!",
                "Pretty useful information.  Thanks!",
                "Fabulous!",
                "Very cool!  Keep up the good work!",
                "Nice description.",
                "Supercool",
                "Bangin project mate!!",
                "Great project!",
                "There are no works for how amazing this is!"
]

# This function will add context to the reply by randomly selecting between
# different arrays of data based on the subreddit.
def reply_on_project(text, title_in, subreddit_in):
    # Check which subreddit we're replying to to add context.
    if(
        subreddit_in == "RASPBERRY_PI_PROJECTS" or
        subreddit_in == "somethingimade" or
        subreddit_in == "diyelectronics"
        ):
        # Check if there's a question mark in the title or the heading.  If there is, it's a question.
        if((text.find("?") > 0) or (title_in.find("?") > 0)):
            return question_replies[random.randint(0,len(question_replies)-1)]
        # If it's a project or link, compliment the project.
        return project_replies[random.randint(0,len(project_replies)-1)]
    # Or if we just need a way to compliment people
    elif(
        subreddit_in == "IDAP" or
        subreddit_in == "itookapicture" or
        subreddit_in == "pics"
        ):
        return compliments_pictures[random.randint(0,len(compliments_pictures)-1)]
    # For the Raspberry Pi sub, we want to check if it's a link, picture, etc.  If it is, return a compliment.
    # If it's not, don't return anything.
    elif(
        subreddit_in == "Raspberry_Pi"
        ):
        if(text == ""):
            return project_replies[random.randint(0,len(project_replies)-1)]
        else:
            return ""

    else:   # And if we're not in a designated sub, then just return a compliment.  What could go wrong?
        return compliments_pictures[random.randint(0,len(compliments_pictures)-1)]


def remove_non_ascii_1(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])

def check_posts_replied_to():
    global posts_replied_to
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))

def subreddit_check(subreddit_in):
    # Get the new subreddits.
    check_posts_replied_to()
    print("STARTING NEW SUBREDDIT: " + str(subreddit_in))
    subreddit = reddit.subreddit(subreddit_in)
    # Check which subreddits have replies.
    # Reply to any subreddits that don't have replies.
    for submission in subreddit.new(limit=50):
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
                    text_in = remove_non_ascii_1(submission.title)
                    submit_text = reply_on_project(submit_text, text_in, subreddit_in)
                    # If the reply on project did not return an empty string then submit it!
                    if submit_text != "":
                        submission.reply(submit_text)
                    with open("posts_replied_to.txt", "a") as f:
                        f.write(submission.id + "\n")
                    print("Sumbitted: " + submit_text)
                    # submission.upvote()     # Upvote this post!
                    time.sleep(5)           # Post was submitted!  Rest 5 seconds.
                    not_submitted = False   # Break out of the loop.s
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
                    if str(e).find("received 403 HTTP response"):
                        print("Got a 403 Response")
                    else:
                        print("Unknown exception:")
                        print(str(e))
                else:
                    debug_api("---------------------------------\n")

    print("Checked the latest.  Sleeping for 1 minutes.")
    time.sleep(1*60)

while True:
    subreddit_check("Raspberry_Pi")
    subreddit_check("IDAP")
    subreddit_check("doodles")
    # subreddit_check("itookapicture") # Banned!
    subreddit_check("RASPBERRY_PI_PROJECTS")
    subreddit_check("somethingimade")
    subreddit_check("diyelectronics")
    subreddit_check("pics")

    print("Completed Full Cycle.  Rest for 30 minutes.")
    time.sleep(30*60)
    # subreddit_check("diy")
#if __name__ == '__main__':
#    main()
