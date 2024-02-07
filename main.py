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

def main():
    # create a client object that interacts with the api
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = youtube_api_key)
    # initialize the watcher and videoID we are tracking
    current_channelID, current_playlistID, current_videoID = video_watcher.initialize_watcher(youtube, 'jubilee')
    dataframeROBERTA, unweightedROBERTA, weightedROBERTA = getSentiments(youtube, current_videoID)
    print('The data type of elements in the Like_Count column is', dataframeROBERTA['Like_Count'].dtype, '!!!\n')
          
    print('Initial Sentiments calculated... start monitoring')
    while(True):
        # overwrite the videoID we are monitoring if it changes.
        current_videoID = video_watcher.start_monitoring(youtube, current_playlistID, current_videoID)
        print('Calculating new sentiments...')
        dataframeROBERTA, unweightedROBERTA, weightedROBERTA = getSentiments(youtube, current_videoID)
        print('Sentiments calculated.\n')
        # now insert the NEW DATA into PSQL connection, also moved old data into the old dataframe
        print('Inserting new values into database')
        initialize_connection(dataframeROBERTA, unweightedROBERTA, weightedROBERTA)
        print('Going to sleep... see you in an hour!\n')
        time.sleep(6000) # sleep for an hour






if __name__ == "__main__":
    main()