from psql_connection import initialize_connection
import pandas as pd

# Adjusted items dictionary with keys matching the column names and values wrapped in lists
items = {
    'Comment_ID': ['UgzDJMB_cbxsFiHK9pV4AaABAg'], 
    'Comment': ['This is fantastic'], 
    'Negative': [0.002422720892354846], 
    'Neutral': [0.014200986362993717], 
    'Positive': [0.9833763241767883],  
    'Like_Count': [22],  # Adjusted key name here to match
    'Sentiment': [0.9809536032844335],
    'weighted_sentiment': [0.9809536032844335]

}

# No need to specify columns if they match the dictionary keys
df = pd.DataFrame(items)

# If you still want to manually specify columns to ensure order or selection, you can do so without suffixes and with corrected Like_Count
df = pd.DataFrame(items, columns=['Comment_ID', 'Comment', 'Negative', 'Neutral', 'Positive', 'Like_Count', 'Sentiment','weighted_sentiment'])

# Display the DataFrame
print(df)

print(df)
initialize_connection(df, 22.22, 27.33)
