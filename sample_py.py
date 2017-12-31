import praw
import pdb
import re
import os

reddit = praw.Reddit('bot1')
 
subreddit = reddit.subreddit("test")


#%% print comments
submissions = list(subreddit.new(limit=5))
    
for sub in submissions:
    sub.comments.replace_more(limit=0)
    for comment in sub.comments.list():
        print(comment.body)


#%%
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []

else:
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))

subreddit = reddit.subreddit('pythonforengineers')
for submission in subreddit.hot(limit=10):
    print(submission.title)

    if submission.id not in posts_replied_to:
        if re.search("i love python", submission.title, re.IGNORECASE):
            submission.reply("Nigerian scammer bot says: It's all about the Bass (and Python)")
            print("Bot replying to : ", submission.title)

            posts_replied_to.append(submission.id)

with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")
