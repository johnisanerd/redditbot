# Happiness Project
The internet is a cynical and unhappy place.  At best your comments are met with silence.  At worst your comments are lambasted and ridiculed.  

This project uses the praw python API to say nice things about people's projects, pictures, and comments.  Spread robot-generated happiness on the internet!

## Subreddits
* /r/RASPBERRY_PI_PROJECTS
* /r/somethingimade
* /r/diyelectronics/
* /r/DIY/
* /r/IDAP/
* /r/itookapicture/
* /r/Raspberry_Pi
* /r/pics/

## To Add:
* /r/Rateme/
* /r/totallynotrobots/

## Improvements Made:
1. Toggle between different subreddits. (Handle multiple subreddits).
1. Look for question marks in the title AND the text body.
5. Add an upvote!  target.upvote()
7. Beef up the reply options. - Added more replies, less roboty!
8. Add in subreddit specific responses, filters.
3. In Raspberry_Pi:  Comment on links shared (To avoid questions or rants).  Now it filters out only for submitted projects.

## Improvements:
9. Plot your karma, bannings, postings over time.
10.  Direct Message Responses:
   * Tell people they are welcome if they say "Thank You."  Maybe add another compliment.
   * If a DM contains "Robot" or "bot" write a random phrase back about being a human.
11.  Add in natural language processing to decide sentiment, generate a quick response.
9. Break your compliments into a mad-lib comment generator.
9. Compliment people on their English "Sorry for my English" -> "You have great English!"
6. Save the comment ID in another file for using it later.
7. Create a readme that shows our work: all the threads replied to!
