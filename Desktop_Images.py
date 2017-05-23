#!/usr/bin/env python3

import praw, urllib.request, os, time
from PIL import Image

# Allows for computer time to connect to wifi if starting up
time.sleep(30)

"""IMPORTANT: FILL IN THESE VARIABLES BELOW"""

#Your reddit username and password
insert_username=''
insert_password=''

# Enter Screen Dimensions. You can also get these from different modules, but I just did it manually
maxwidth=2880
maxheight=1800

#"curfolder" is a subfolder of "folderpath"
#"curfolder" will hold the newly scraped images each day
#"folderpath", depending if the variable keep=True or keep=False, the previous day's images will be stored in a separate folder from curfolder
folderpath="/Users/WillC/Pictures/Will's Desktop Pictures/"
curfolder="/Users/WillC/Pictures/Will's Desktop Pictures/Current Desktop Photos/"

"""IMPORTANT: FILL IN THESE VARIABLES ABOVE"""

#There is a quick intro on how to use praw. It's very easy to look up
reddit = praw.Reddit(client_id='auEVwX9t9sFF7A',
                     client_secret='zxmzCiOsFgwtMwfIvRRHaZsJU8s',
                     user_agent='EarthPorn_Scrape',
                     username=insert_username,
                     password=insert_password)

#choose your subreddit. You can edit the code so it scrapes from multiple subreddits if desired
subreddit = reddit.subreddit('EarthPorn')

curphotos=os.listdir(curfolder)
listdir=os.listdir(folderpath)
newweeklyfolder=""
count=0 # count number of acceptable images

widthToheight=maxwidth/maxheight
pixelcount=maxwidth*maxheight

#function looks for things that can't be included in file names
def ChangeTitle(pretitle):
    searchfor=["!","@","#","$","%","^","&","*","(",")","+","[","]","{","}","/","\\","~","`",",",".","?","<",">"]
    for c in searchfor:
        pretitle=pretitle.replace(c,"a")
    return pretitle

#function gets the appropriate image size ratio to fit your screen and allows only set minimum resolution
def ConfirmSize(path):
    img=Image.open(path,'r')
    width=img.width
    height=img.height
    imgwidthToheight=width/height
    imgpixelcount=width*height

    if ((imgwidthToheight<(widthToheight-0.30) or imgwidthToheight>widthToheight+0.50) or imgpixelcount<pixelcount*0.6):
        os.remove(path)
        return False
    return True

"""
If keep==True, a new folder will be created to hold previous images.
If keep==False, previous images will not be kept.
"""
keep=False
# 1. create new folder to hold old images if wanted
if keep==True:
    for i in range(1,len(listdir)):
        if os.path.exists(folderpath+str(i)) == False:
            os.makedirs(folderpath+str(i))
            newweeklyfolder = folderpath+s
            str(i)+"/"
            break

# 2. download images to current desktop photos and maintain dimension restrictions
maxImages=10
for submission in subreddit.hot(limit=maxImages*10):
    source=submission.url
    title = ChangeTitle(submission.title)
    if len(title)>250:
        title=title[0:250]

    if ".jpg" in source:
        ext=".jpg"
    elif ".png" in source:
        ext = ".png"
    elif ".jpeg" in source:
        ext = ".jpeg"
    else:
        continue

    fullpath=curfolder+title+ext

    urllib.request.urlretrieve(source, fullpath)
    if (ConfirmSize(fullpath)==True):
        count+=1
    if (count==maxImages):
        break


#3. move all images in current desktop photos to new weekly folder
if keep==True:
    for photo in curphotos:
        os.rename(curfolder+photo, newweeklyfolder+photo)
else:
    for photo in curphotos:
        os.remove(curfolder+photo)