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


# master method that gets all the current video ids in a set
def getAllPlaylistItems(youtube, channelName):
    # get the channel ID
    channelId = getChannelId_with_SEARCH(youtube, channelName)

    # get the upload playlist ID
    uploadsPlaylistId = getPlaylistId_with_channelId(youtube, channelId)

    # use that ID, to retrieve all videos within it (it's a generator item)
    videoId_gen = getAllVideoIds_with_uploadsPlaylistId(youtube, uploadsPlaylistId)

    videoId_list = []
    for i in videoId_gen:
        videoId_list.append(i)
    return videoId_list



# first get the playlist Id of the 'uploads' playlist with the 'search' command - (100 quota) don't abuse this!
def getChannelId_with_SEARCH(youtube, channelName):
    request = youtube.search().list(
        part="snippet",
        channelType="any",
        q=channelName
    )
    response = request.execute()
    # return just the channelId
    return response['items'][0]['snippet']['channelId']

# now get the upload playlist Id with the channelId
def getPlaylistId_with_channelId(youtube, channelId):
    request = youtube.channels().list(
        part="contentDetails",
        id=channelId
    )
    response = request.execute()
    # return the playlistID
    return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

# below are methods to retrieve videoId and video datetime information through the uploadsPlaylistId
#-----------------------#-----------------------#-----------------------#-----------------------#-----------------------#-----------------------


# retrieves video information using specific page_token.
def get_PlaylistItems_from_uploadPlayListId(youtube, uploadPlaylistId, page_token=None):
    # request information
    request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=uploadPlaylistId,
        pageToken=page_token,
        maxResults=100,
    )
    response = request.execute()
    # put response into variable (after parsing)
    return response

# method to retrieve all videos in a playlist, going to next page if needed.
def getAllVideoIds_with_uploadsPlaylistId(youtube, uploadPlaylistId, page_token=None):
    payload = get_PlaylistItems_from_uploadPlayListId(youtube, uploadPlaylistId, page_token)
    for item in payload["items"]:
        yield item['contentDetails']  

    next_page_token = payload.get("nextPageToken")
    if next_page_token is not None:
        yield from getAllVideoIds_with_uploadsPlaylistId(youtube, uploadPlaylistId, next_page_token)










def checkforNewVideos(youtube, lastCheckpointVideos=set()):
    
