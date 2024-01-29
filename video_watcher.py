import requests
import time
import json
from datetime import datetime, timedelta


# logic:
# when initialized, run a query to get all the videos currently in a channel, and save it as a base line 'old_videos'

# this file will then conduct routine API calls to get all the videos currently in a channel and 
# check if there is a difference in the videos returned

# if there is a difference, then that must mean a new video has been uploaded. 
# we will then store the video ID of said video, and run a sentiment calculation after a set period of time.


# master method that gets all the current video id's in a list
def getAllVideoIds(youtube, channelName):
    # get the upload playlist ID
    uploadsPlaylistId = getUploadsPlaylistId(youtube, channelName)
    # use that ID, to retrieve all videos within it (it's a generator item)
    videoId_gen = get_all_videoIds_in_uploadPlayList(youtube, uploadsPlaylistId)
    old_videoId_list = []
    for i in videoId_gen:
        old_videoId_list.append(i)
    return old_videoId_list

# get the playlist Id of the 'uploads' playlist.
def getUploadsPlaylistId(youtube, channelName):
    request = youtube.channels().list(
        part="contentDetails",
        forUsername=channelName
    )
    response = request.execute()
    # etag field is the Channel ID
    return response['items'][-1]['contentDetails']['relatedPlaylists']['uploads']

def get_videoIds_from_uploadPlayListId(youtube, uploadPlaylistId, page_token=None):
    # request information
    request = youtube.playlistItems().list(
        part="id",
        playlistId=uploadPlaylistId,
        pageToken=page_token,
        maxResults=100,
    )
    response = request.execute()
    # put response into variable (after parsing)
    return response

# method to retrieve all items in the playlist, going to next page if needed.
# *returns lots of dicts*
def get_all_videoIds_in_uploadPlayList(youtube, uploadPlaylistId, page_token=None):
    payload = get_videoIds_from_uploadPlayListId(youtube, uploadPlaylistId, page_token)
    for item in payload["items"]:
        yield item['id']  

    next_page_token = payload.get("nextPageToken")
    if next_page_token is not None:
        yield from get_all_videoIds_in_uploadPlayList(youtube, uploadPlaylistId, next_page_token)


def checkVideos(youtube, ):