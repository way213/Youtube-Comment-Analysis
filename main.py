import os
import time
import googleapiclient.discovery
from extract_sentiment import getSentiments
import video_watcher 

# here is our API key and other items
youtube_api_key = 'AIzaSyBaFhDvztf8hwgX4DWxTRdbmcqKbEkr6-A'
api_service_name = "youtube"
api_version = "v3"

def main():
    # create a client object that interacts with the api
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = youtube_api_key)

    current_videoID = video_watcher.initialize_watcher(youtube, 'Some Channel')
    while(True):
        # overwrite the video we are monitoring if it changes.
        current_videoID = video_watcher.start_monitoring(youtube, current_videoID)
        dataframeVADER, unweightedVADER, weightedVADER, dataframeROBERTA, unweightedROBERTA, weightedROBERTA = getSentiments(youtube, current_videoID)
        ##### SOME METHOD TO INSERT INTO PSQL
        
        time.sleep(6000) # sleep for an hour






if __name__ == "__main__":
    main()