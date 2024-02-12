import requests
import time
import json
from datetime import datetime, timedelta
from requests.exceptions import HTTPError


# logic:
# when initialized, run a query to get the upload playlist, and set the first result as our current monitoring video.

#we will conduct routine API calls to get the most recent video in a channel and 
# check if there is a difference.

# if there is a difference, then that must mean a new video has been uploaded. 
# we will then store the video ID of said video, and run a sentiment calculation on it.


# method that initializes our monitoring process
def initialize_watcher(youtube, channelName):
    try:
        channelID = getChannelId_with_SEARCH(youtube, channelName)
    except HTTPError as http_err:
    # Check if the error is a 403 Client Error and contains 'quotaExceeded'
        if http_err.response.status_code == 403:
            print("Error: The request cannot be completed because you have exceeded your quota.")
        else:
            print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print('Retrieved Channel ID!')
    
    try:
        playlistID = getPlaylistId_with_channelId(youtube, channelID)
    except HTTPError as http_err:
    # Check if the error is a 403 Client Error and contains 'quotaExceeded'
        if http_err.response.status_code == 403:
            print("Error: The request cannot be completed because you have exceeded your quota.")
        else:
            print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print('Retrieved Upload Playlist ID!')
    
    try:
        videoID, videoTitle = get_most_recent_video(youtube, playlistID)
    except HTTPError as http_err:
    # Check if the error is a 403 Client Error and contains 'quotaExceeded'
        if http_err.response.status_code == 403:
            print("Error: The request cannot be completed because you have exceeded your quota.")
        else:
            print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print('Retrieved most recent video ID!')
        return channelID, playlistID, videoID, videoTitle



def start_monitoring(youtube, playlistID, current_videoID):
    try:
        recent_videoID, recent_videoTitle = get_most_recent_video(youtube, playlistID)
    except HTTPError as http_err:
    # Check if the error is a 403 Client Error and contains 'quotaExceeded'
        if http_err.response.status_code == 403:
            print("Error: The request cannot be completed because you have exceeded your quota.")
        else:
            print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print('Retrieved most recent video ID!')
    # Check if the video currently being monitored is the most recent one or not.
    if (current_videoID != recent_videoID): 
        print('New video Detected...!')
        return recent_videoID, recent_videoTitle
    else:
        print('No new videos uploaded...!')
        return recent_videoID, recent_videoTitle






# first get the channel Id of the 'uploads' playlist with the 'search' command - (100 quota) don't abuse this!
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

def get_most_recent_video(youtube, uploadPlaylistId, page_token=None):
    # request information
    request = youtube.playlistItems().list(
        part="contentDetails,snippet",
        playlistId=uploadPlaylistId,
        pageToken=page_token,
        maxResults=1,
    )
    response = request.execute()
    # return the videoId, and the title of the video
    return response['items'][0]['contentDetails']['videoId'], response['items'][0]['snippet']['title']



# unused methods below...
#-----------------------#-----------------------#-----------------------#-----------------------#-----------------------#-----------------------






#  method that gets all the current video ids in a playlist
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
    return response

# method to retrieve all videos in a playlist, going to next page if needed.
def getAllVideoIds_with_uploadsPlaylistId(youtube, uploadPlaylistId, page_token=None):
    payload = get_PlaylistItems_from_uploadPlayListId(youtube, uploadPlaylistId, page_token)
    for item in payload["items"]:
        yield item['contentDetails']  

    next_page_token = payload.get("nextPageToken")
    if next_page_token is not None:
        yield from getAllVideoIds_with_uploadsPlaylistId(youtube, uploadPlaylistId, next_page_token)
    
