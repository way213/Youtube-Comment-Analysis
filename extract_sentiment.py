import os
import googleapiclient.discovery
import extract_comments
import vader_calculations
import roberta_calculations

def getSentiments(youtube, videoId):
    # get the comments
    comments = extract_comments.getLinkedLists(youtube, videoId)
    # do calculations for VADER
    dataframeVADER, unweightedVADER, weightedVADER = vader_calculations.get_Vader_results(comments)
    # do calculations for Roberta
    dataframeROBERTA, unweightedROBERTA, weightedROBERTA = roberta_calculations.get_ROBERTA_results(comments)

    return dataframeVADER, unweightedVADER, weightedVADER, dataframeROBERTA, unweightedROBERTA, weightedROBERTA

