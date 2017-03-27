#!/usr/bin/env python3

import praw, urllib.request, os

insert_username='Wills_Python"
insert_password="Wills_Python"

reddit = praw.Reddit(client_id='auEVwX9t9sFF7A',
                     client_secret='zxmzCiOsFgwtMwfIvRRHaZsJU8s',
                     user_agent='EarthPorn_Scrape',
                     username=insert_username,
                     password=insert_password)

subreddit = reddit.subreddit('EarthPorn')

folderpath="/Users/WillC/Pictures/Will's Desktop Pictures/"
curfolder="/Users/WillC/Pictures/Will's Desktop Pictures/Current Desktop Photos/"
curphotos=os.listdir(curfolder)
listdir=os.listdir(folderpath)
newweeklyfolder=""

def ChangeTitle(pretitle):
    searchfor=["!","@","#","$","%","^","&","*","(",")","+","[","]","{","}","/","\\","~","`",",",".","?","<",">"]
    for c in searchfor:
        pretitle=pretitle.replace(c,"_")
    return pretitle

# 1. create new weekly folder
for i in range(1,len(listdir)):
    if os.path.exists(folderpath+str(i)) == False:
        os.makedirs(folderpath+str(i))
        newweeklyfolder = folderpath+str(i)+"/"
        break

# 2. download images to current desktop photos
for submission in subreddit.top(time_filter="week",limit=20):
    source=submission.url
    title = ChangeTitle(submission.title)
    if len(title)>250:
        title=title[0:250]

    if ".jpg" in source:
        urllib.request.urlretrieve(source, curfolder + title + ".jpg")

# 3. move all images in current desktop photos to new weekly folder
for photo in curphotos:
    os.rename(curfolder+photo, newweeklyfolder+photo)

