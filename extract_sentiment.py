import os
import googleapiclient.discovery
import extract_comments
import roberta_calculations

def getSentiments(youtube, videoId):
    # get the comments
    comments = extract_comments.getLinkedLists(youtube, videoId)
    # do calculations for Roberta
    dataframeROBERTA, unweightedROBERTA, weightedROBERTA = roberta_calculations.get_ROBERTA_results(comments)
    return dataframeROBERTA, unweightedROBERTA, weightedROBERTA

