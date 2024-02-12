from operator import itemgetter
import os
import time
import googleapiclient.discovery
from extract_sentiment import getSentiments
from psql_connection import initialize_connection
import video_watcher 
import configparser
from operator import itemgetter


# here is our API key and other items
config = configparser.ConfigParser()
config.read('youtube_api.ini')
youtube_api_key = itemgetter('youtube_api_key')(config['api'])
api_service_name = "youtube"
api_version = "v3"


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


youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = youtube_api_key)
uploadPlaylistId = 'UUqnbDFdCpuN8CMEg0VuEBqA'
x, y = get_most_recent_video(youtube, uploadPlaylistId, page_token=None)

print(x,'heres the videoID\n')
print(y)