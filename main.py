import os
import time
import googleapiclient.discovery
from extract_sentiment import getSentiments
from psql_connection import initialize_connection
import video_watcher 

# here is our API key and other items
youtube_api_key = 'AIzaSyBaFhDvztf8hwgX4DWxTRdbmcqKbEkr6-A'
api_service_name = "youtube"
api_version = "v3"

def main():
    # create a client object that interacts with the api
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = youtube_api_key)
    # initialize the watcher and videoID we are tracking
    current_videoID = video_watcher.initialize_watcher(youtube, 'Some Channel')
    dataframeROBERTA, unweightedROBERTA, weightedROBERTA = getSentiments(youtube, current_videoID)

    while(True):
        # overwrite the video we are monitoring if it changes.
        current_videoID = video_watcher.start_monitoring(youtube, current_videoID)
        dataframeROBERTA, unweightedROBERTA, weightedROBERTA = getSentiments(youtube, current_videoID)
        # now insert the NEW DATA into PSQL connection, also moved old data into the old dataframe
        initialize_connection(dataframeROBERTA)


        time.sleep(6000) # sleep for an hour






if __name__ == "__main__":
    main()