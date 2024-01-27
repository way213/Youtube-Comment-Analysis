from objects import comment_details, CommentNode, CommentLinkedList

# master method that gets all the comments for further analysis, calls the other methods within this file as well
# returns the list of all the comments in a linkedlist format in the list
def getLinkedLists(youtube, videoId):
    # method call
    our_response = get_comment_via_videoID(youtube, videoId)
    # empty list to store the payload items 
    our_response_list =[]
    # get items out from payload
    for item in our_response:
        our_response_list.append(item)

    # empty list to store all top-level-comments
    stored_details = []
    # store objects of comment details into empty list
    for i in range(len(our_response_list)):
        toplevelcomment = our_response_list[i]['snippet']['topLevelComment']['snippet']
        stored_details.append(
            comment_details(our_response_list[i]['id'],
                            toplevelcomment['textDisplay'],
                            toplevelcomment['textOriginal'],
                            toplevelcomment['likeCount']))

    # empty list to store all the linkedlists 
    all_linked_lists = []
    for top_level_comments in stored_details:
        # create a linked list for each top-level comment
        comment_list = CommentLinkedList()
        # head node
        head = CommentNode(top_level_comments[1], top_level_comments[2], top_level_comments[3])
        comment_list.add_comment(head)
        
        # the replies
        replies = getReplies(youtube, top_level_comments[0])
        for reply in replies:
            # make node for each comment
            reply_node = CommentNode(reply['snippet']['textDisplay'], reply['snippet']['textOriginal'], reply['snippet']['likeCount'])
            comment_list.add_comment(reply_node)

        # add the completed linked list to the list
        all_linked_lists.append(comment_list)
    
    return all_linked_lists

def get_comment_via_videoID(youtube, videoId, pageToken=''):
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=videoId,
        maxResults=100,
        pageToken=pageToken
    )
    payload = request.execute()
    yield from payload["items"]
    # get the next page token, if there is one - which indicates there is another page.
    next_page_token = payload.get("nextPageToken")
    if next_page_token is not None:
        # recursion
        yield from get_comment_via_videoID(youtube, videoId, next_page_token)
        
    # we return a dict here of top-level-comments
    return payload

def getReplies(youtube, videoId, pageToken=''):
    request = youtube.comments().list(
        part="snippet",
        maxResults=100,
        parentId=videoId,
        pageToken=pageToken
    )
    payload = request.execute()
    yield from payload["items"]
    # get the next page token, if there is one - which indicates there is another page.
    next_page_token = payload.get("nextPageToken")
    if next_page_token is not None:
        # recursion
        yield from getReplies(youtube, videoId, next_page_token)

    # we return a dict here of top-level-comments
    return payload

