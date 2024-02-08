import numpy as np
import pandas as pd
# Hugging face - gets sarcasm
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax

# we will use a pre-trained model for this
MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

def get_ROBERTA_results(all_linked_lists):
    ROBERTA_df = pd.DataFrame()
    print('analyzing comment thread')
    for i in range(len(all_linked_lists)):
        temp = analyze_comments_ROBERTA(all_linked_lists[i])
        ROBERTA_df = pd.concat([ROBERTA_df, temp], axis=0, ignore_index=True)

    # first let us get the total amount of likes within the entire comment section
    total_likes_in_comment_section = 0
    for linked_list in all_linked_lists:
        total_likes_in_comment_section+=linked_list.total_likes

    # now let's get the sentiment scores for ROBERTA
    ROBERTA_df['Sentiment'] = ROBERTA_df.apply(get_sentiment, axis=1)
    unweighted_ROBERTA_result = round(ROBERTA_df['Sentiment'].mean(),3)
    ROBERTA_df['weighted_sentiment'] = ROBERTA_df.apply(multiply_columns, axis=1)
    weighted_ROBERTA_result = round(ROBERTA_df['weighted_sentiment'].sum()/total_likes_in_comment_section , 2)

    return ROBERTA_df, unweighted_ROBERTA_result, weighted_ROBERTA_result


# Function to traverse the LinkedList and conduct sentiment analysis with ROBERTA
def analyze_comments_ROBERTA(linked_list):
    comments_data = []
    current = linked_list.head
    while current:
        encoded_text = tokenizer(current.text_original, return_tensors='pt', max_length=512, truncation=True)
        output = model(**encoded_text)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        # Round the scores to 4 decimal places
        scores = np.round(scores, 4)
        items = {
        'Comment_ID': current.comment_id,
        'Comment': current.text_original,
        'Negative': scores[0],
        'Neutral': scores[1],
        'Positive': scores[2],
        'Like_Count': current.like_count
        }
        comments_data.append(items)
        # Traverse linked list
        current = current.next

    df = pd.DataFrame(comments_data, columns=['Comment_ID','Comment','Negative','Neutral','Positive','Like_Count'])
    return df

# Define a function to calculate sentiment score for ROBERTA
def get_sentiment(row):
    return ((-1) * row['Negative'] + row['Positive'])

# Define a function to multiply sentiment and like_count and return the result
def multiply_columns(row):
    return row['Sentiment'] * row['Like_Count']
