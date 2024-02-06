import numpy as np
import pandas as pd
# VADER - doesn't get sarcasm
from nltk.sentiment import SentimentIntensityAnalyzer
from tqdm.notebook import tqdm
# download the datasets/models from nltk
import nltk
nltk.download('vader_lexicon')

def get_Vader_results(all_linked_lists):
    # Initialize empty dataframe
    VADER_df = pd.DataFrame()

    # Analyze the comments and get the DataFrame
    for i in range(len(all_linked_lists)):
        print('analyzing comment thread', i)
        # Get the individual scores
        temp = analyze_comments_VADER(all_linked_lists[i])  
        VADER_df = pd.concat([VADER_df, temp], axis=0, ignore_index=True)

    unweighted_VADER_result = VADER_df['Sentiment'].mean()

    # first let us get the total amount of likes within the entire comment section
    total_likes_in_comment_section = 0
    for linked_list in all_linked_lists:
        total_likes_in_comment_section+=linked_list.total_likes

    VADER_df['weighted_sentiment'] = VADER_df.apply(multiply_columns, axis=1)
    weighted_VADER_result = VADER_df['weighted_sentiment'].sum()/total_likes_in_comment_section

    return VADER_df, unweighted_VADER_result, weighted_VADER_result

# Function to traverse the LinkedList and conduct sentiment analysis without weights
def analyze_comments_VADER(linked_list):
    analyzer = SentimentIntensityAnalyzer()
    comments_data = []

    current = linked_list.head
    while current:
        scores = analyzer.polarity_scores(current.text_original)
        # Calculate non-weighted scores
        non_weighted_scores = {
                'Comment_ID':current.comment_id,
                'Comment': current.text_original,
                'Negative': scores['neg'],
                'Neutral': scores['neu'],
                'Positive': scores['pos'],
                'Sentiment': scores['compound'],
                'Like Count': current.like_count
        }
        comments_data.append(non_weighted_scores)
        # Traverse linked list
        current = current.next

    df = pd.DataFrame(comments_data, columns=['Comment_ID', 'Comment', 'Negative', 'Neutral', 'Positive', 'Sentiment', 'Like Count'])
    return df


# Define a function to multiply sentiment and like_count and return the result
def multiply_columns(row):
    return row['Sentiment'] * row['Like Count']





