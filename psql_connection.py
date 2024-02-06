import configparser
from operator import itemgetter
import pandas as pd
import sqlalchemy
from sqlalchemy import DATETIME, create_engine, Column, Integer, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

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
    avg_unweighted = Column(DECIMAL(4,3))    
    avg_weighted = Column(DECIMAL(4,3))    
    time_recorded = Column(DATETIME)

def initialize_connection(df):
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
        insert_dataframe(df, session)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()
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
        return engine
    except Exception as e:
        print('Error occured: {e}')


def create_session(engine):
    try:
        Session = sessionmaker(bind=engine)
        return Session()
    except Exception as e:
        print('Error occured: {e}')


def insert_dataframe(df, session):
    try:
        data = df.to_dict(orient='records')
        session.bulk_insert_mappings(NewCommentDetails, data)
        session.commit()
        print("New comments data successfully inserted into the database.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"An error occurred during data insertion: {e}")

# method that transports the data in the newcomments dataframe into the odcomments dataframe
def replace_old_with_new_comments(session):
    try:
        # Step 1: Read data from NewCommentDetails into a DataFrame
        new_comments_df = pd.read_sql(session.query(NewCommentDetails).statement, session.bind)
        
        # Step 2: Clear OldCommentDetails table
        session.query(OldCommentDetails).delete()
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
        session.rollback()  # Rollback the changes on error
        print(f"An error occurred during the replacement process: {e}")
