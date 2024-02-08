import configparser
from operator import itemgetter
import pandas as pd
import sqlalchemy
from sqlalchemy import DATETIME, TIMESTAMP, create_engine, Column, Integer, String, DECIMAL, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


# Global Base declaration
Base = declarative_base()

class OldCommentDetails(Base):
    __tablename__ = 'old_results'
    Comment_ID = Column(String, primary_key=True)
    Comment = Column(String)
    Negative = Column(DECIMAL(4,3))
    Neutral = Column(DECIMAL(4,3))
    Positive = Column(DECIMAL(4,3))    
    Like_Count = Column(Integer)
    Sentiment = Column(DECIMAL(4,3))    
    weighted_sentiment = Column(DECIMAL(6,3))

class NewCommentDetails(Base):
    __tablename__ = 'new_results'
    Comment_ID = Column(String, primary_key=True)
    Comment = Column(String)
    Negative = Column(DECIMAL(4,3))
    Neutral = Column(DECIMAL(4,3))
    Positive = Column(DECIMAL(4,3))    
    Like_Count = Column(Integer)
    Sentiment = Column(DECIMAL(4,3))    
    weighted_sentiment = Column(DECIMAL(6,3))

class OverallSentiments(Base):
    __tablename__ = 'average_sentiments'
    id = Column(Integer, primary_key=True)
    avg_unweighted = Column(DECIMAL(6,2))    
    avg_weighted = Column(DECIMAL(6,2))    
    time_recorded = Column(TIMESTAMP)

def initialize_connection(df, unweighted, weighted):
    session = None  # Initialize session to None
    engine = None  # Initialize engine to None
    try:
        # start engine
        engine = start_engine()
        # create the tables
        Base.metadata.create_all(engine)
        # create session
        session = create_session(engine)

        # move new comments into old checkpoint
        replace_old_with_new_comments(session)

        # insert into database
        insert_dataframe(session, df)
        
        print('completed dataframe transfer')
        insert_calculations(session, unweighted, weighted)
    except Exception as e:
        print(f"An error occurred in method 'initialize_connection': {e}")
    finally:
        if session:
            session.close()
        if engine:
            engine.dispose()
        print("Session and engine disposed.")


def start_engine():
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        u, pw, host, db = itemgetter('username', 'password', 'host', 'database')(config['db'])
        dsn = f'postgresql://{u}:{pw}@{host}/{db}'
        print(f'using dsn: {dsn}')
        engine = create_engine(dsn, echo=True)
        print('Engine created!')
        return engine
    except Exception as e:
        print('Error occured during engine creation: {e}')


def create_session(engine):
    try:
        Session = sessionmaker(bind=engine)
        print('Session created!')
        return Session()
    except Exception as e:
        print('Error occured during session creation: {e}')


def insert_dataframe(session, df):
    try:
        data = df.to_dict(orient='records')
        session.bulk_insert_mappings(NewCommentDetails, data)
        session.commit()
        print("New comment data successfully inserted into the database.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"An error occurred during dataframe insertion: {e}")

# method to insert sentiment calculations into database
def insert_calculations(session, unweighted, weighted):
    try:
        # create object to insert
        new_record = OverallSentiments(
            avg_unweighted=unweighted,
            avg_weighted=weighted,
            time_recorded=datetime.now()
        )
        
        # Add the new record to the session and commit it
        session.add(new_record)
        session.commit()
        print("Sentiment data successfully inserted into the database.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"An error occurred during data insertion: {e}")


# method that transports the data in the newcomments dataframe into the odcomments dataframe
def replace_old_with_new_comments(session):
    try:
        # Step 1: Read data from NewCommentDetails into a DataFrame
        new_comments_df = pd.read_sql(session.query(NewCommentDetails).statement, session.connection())
        print('HERE IS THE DATAFRAM:', new_comments_df)

        # Step 2: Clear New and OldCommentDetails table
        session.query(OldCommentDetails).delete()
        session.query(NewCommentDetails).delete()
        session.commit()
        
        # Step 3: Insert data from DataFrame into OldCommentDetails
        if not new_comments_df.empty:
            data = new_comments_df.to_dict(orient='records')
            session.bulk_insert_mappings(OldCommentDetails, data)
            session.commit()
            print("Successfully moved data from NewCommentDetails to OldCommentDetails.")
        else:
            print("No data found in NewCommentDetails to move.")

    except SQLAlchemyError as e:
        print(f"An error occurred during the replacement process: {e}")
        session.rollback()  # Rollback the changes on error
