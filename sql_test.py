from psql_connection import initialize_connection
import pandas as pd

# Adjusted items dictionary with keys matching the column names and values wrapped in lists
items = {
    'comment_id': ['UgzDJMB_cbxsFiHK9pV4AaABAg'], 
    'comment': ['This is fantastic'], 
    'negative': [0.002], 
    'neutral': [0.014], 
    'positive': [0.983],  
    'like_Count': [22],  # Adjusted key name here to match
    'sentiment': [0.980],
    'weighted_sentiment': [0.980],
    'worded_sentiment' : ['Good']

}

# No need to specify columns if they match the dictionary keys
df = pd.DataFrame(items)

# If you still want to manually specify columns to ensure order or selection, you can do so without suffixes and with corrected Like_Count
df = pd.DataFrame(items, columns=['comment_ID', 'comment', 'negative', 'neutral', 'positive', 'like_count', 'sentiment','weighted_sentiment','worded_sentiment'])

# Display the DataFrame

print(df)
initialize_connection(df, 22.22, 27.33)
