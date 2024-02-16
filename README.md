# Video Comment Sentiment Analysis

## Project Overview

This project aims to analyze sentiment from comments on video content, focusing on a specific channel's most recent videos. By performing routine API calls to fetch comments, the project applies sentiment analysis to gauge the overall sentiment of the audience's reactions. This analysis can provide valuable insights into viewers' perceptions, contributing to content strategy adjustments and enhancing viewer engagement.

## Features

- **Automated Comment Fetching:** Routine API calls to retrieve comments from the most recent videos of a specified channel.
- **Sentiment Analysis:** Application of sentiment analysis algorithms on fetched comments to determine overall sentiment (positive, negative, neutral).
- **Database Storage:** Efficient storage of channels, videos, comments, sentiment analysis results, and fetch iterations in a structured database.
- **Dynamic Updates:** The database is designed to accommodate new comments and videos, ensuring the analysis is up-to-date with the latest viewer interactions.

## Database Design

The database is structured to normalize the data and reduce redundancy, organized into the following tables:

- **channels:** Stores information about each channel.
- **videos:** Contains details of videos published by channels, linked to the `channels` table.
- **comments:** Holds comments made on videos, linked to the `videos` table.
- **sentimentanalysis:** Stores the sentiment analysis result for each comment, linked to the `comments` table.
- **iterations:** Tracks each iteration of comment fetching for videos, linked to the `videos` table.

### Relationships

- A **channel** can have multiple **videos**.
- A **video** can have multiple **comments**.
- Each **comment** has a unique **sentiment analysis** result.
- Each **video** can be associated with multiple **iterations** of comment fetching.

### ERD

Please refer to the Entity-Relationship Diagram (ERD) included in the repository for a visual representation of the database structure and relationships.

Please note that the relationship for the tables sentiment analysis and comment are **ONE to ONE** PSQL ERD diagrams do not support one to one relationships hence why it is shown this way.
<img width="954" alt="Screenshot 2024-02-15 at 7 54 14 PM" src="https://github.com/way213/Youtube-Comment-Analysis/assets/108505154/826290c7-4548-4e60-8f61-717194db24be">

## Getting Started

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/videocommentsentiment.git

