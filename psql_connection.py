import configparser
from operator import itemgetter

import sqlalchemy
from sqlalchemy import create_engine

# columns and their types, including fk relationships
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

# declarative base, session, and datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime


import psycopg2

import psycopg2

try:
    # Connect to your PostgreSQL database
    conn = psycopg2.connect(
        dbname='homework06',
        user='williamyang',
        password='admin',
        host='localhost'
    )
    print("Connected to the database.")

    # Create a cursor object
    cur = conn.cursor()
    print("Cursor created.")

    # Your database operations go here

    # Close the cursor
    cur.close()
    print("Cursor closed.")

    # Close the connection
    conn.close()
    print("Connection closed.")

except Exception as e:
    print("Connection error:", e)


    
#INSERT INTO comments_table (comment_id, text, like_count, sentiment, ...)
#VALUES ('new_comment_id', 'comment_text', new_like_count, 'sentiment_result', ...)
#ON CONFLICT (comment_id)
#DO
#   UPDATE SET like_count = EXCLUDED.like_count,
#              -- Add any other fields that might change and need to be updated
#WHERE comments_table.like_count <> EXCLUDED.like_count;
