import os
import googleapiclient.discovery
from extract_sentiment import getSentiments
# here is our API key and other items
youtube_api_key = 'AIzaSyBaFhDvztf8hwgX4DWxTRdbmcqKbEkr6-A'
api_service_name = "youtube"
api_version = "v3"
videoId = 'C2ati-TugBU'

def main():
    # create a client object that interacts with the api
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = youtube_api_key)

    ##### method that returns videoId of new video after certian timeframe

    dataframeVADER, unweightedVADER, weightedVADER, dataframeROBERTA, unweightedROBERTA, weightedROBERTA = getSentiments(youtube, videoId)





if __name__ == "__main__":
    main()