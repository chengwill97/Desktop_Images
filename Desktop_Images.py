#!/usr/bin/env python3

import praw
import urllib.request
import os
import time
from PIL import Image

#----------------------------------------------------------------------

# IMPORTANT: FILL IN THESE VARIABLES BELOW

# Your reddit username and password
insert_username = 'Wills_Python'
insert_password = 'Wills_Python'

# Enter Screen Dimensions. You can also get these from different modules, but I just did it manually
maxwidth = 2880
maxheight = 1800

# "curfolder" is a subfolder of "folderpath" and will hold the newly scraped images each day
# "folderpath", depending if the variable KEEP = True or KEEP = False, the previous day's images will be stored in a
# separate folder from curfolder
folderpath = "/Users/WillC/Pictures/Will's Desktop Pictures/"
curfolder = "/Users/WillC/Pictures/Will's Desktop Pictures/Current Desktop Photos/"

# IMPORTANT: FILL IN THESE VARIABLES ABOVE

#----------------------------------------------------------------------

# Allows for computer time to connect to wifi if starting up
#time.sleep(30)

# There is a quick intro on how to use praw. It's very easy to look up
reddit = praw.Reddit(client_id='auEVwX9t9sFF7A',
                     client_secret='zxmzCiOsFgwtMwfIvRRHaZsJU8s',
                     user_agent='EarthPorn_Scrape',
                     username=insert_username,
                     password=insert_password)

curphotos = os.listdir(curfolder)
listdir = os.listdir(folderpath)
newweeklyfolder = ""

widthtoheight = maxwidth / maxheight
pixelcount = maxwidth * maxheight


# function looks for things that can't be included in file names
def changetitle(pretitle):
    searchfor = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", " + ", "[", "]", "{", "}", "/", "\\", "~", "`", ",",
                 ".", "?", "<", ">"]
    for c in searchfor:
        pretitle = pretitle.replace(c, "_")
    return pretitle


# function gets the appropriate image size ratio to fit your screen and allows only set minimum resolution
def confirmsize(path):
    img = Image.open(path, 'r')
    width = img.width
    height = img.height
    imgwidthtoheight = width / height
    imgpixelcount = width * height

    if ((imgwidthtoheight < (widthtoheight - 0.40)
            or imgwidthtoheight > (widthtoheight + 0.70))
            or imgpixelcount < pixelcount * 0.4):
        os.remove(path)
        return False
    return True

"""
If KEEP == True, a new folder will be created to hold previous images.
If KEEP == False, previous images will not be kept.
"""
KEEP = False
# 1. create new folder to hold old images if wanted
if KEEP:
    for i in range(1, len(listdir)):
        if not os.path.exists(folderpath + str(i)):
            os.makedirs(folderpath + str(i))
            newweeklyfolder = folderpath + str(i) + "/"
            break

# 2. download images to current desktop photos and maintain dimension restrictions
subredditNames = ['EarthPorn', 'ImaginaryLandscapes']
maxImages = 5 * len(subredditNames)

for subredditName in subredditNames:
    count = 0
    subreddit = reddit.subreddit(subredditName)
    for submission in subreddit.hot(limit=(maxImages * 25)):
        source = submission.url
        title = subredditName + '_' + changetitle(submission.title)

        title = title[0:min(len(title),250)]

        if ".jpg" in source:
            ext = ".jpg"
        elif ".png" in source:
            ext = ".png"
        elif ".jpeg" in source:
            ext = ".jpeg"
        else:
            continue

        fullpath = curfolder + title + ext

        try:
            urllib.request.urlretrieve(source, fullpath)
            if (confirmsize(fullpath)):
                count += 1
        except:
            pass
        if (count == round(maxImages / len(subredditNames))):
            break

# 3. move all images in current desktop photos to new weekly folder
if KEEP == True:
    for photo in curphotos:
        os.rename(curfolder + photo, newweeklyfolder + photo)
else:
    for photo in curphotos:
        os.remove("{0}{1}".format(curfolder, photo))
