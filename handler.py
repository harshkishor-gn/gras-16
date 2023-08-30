import json
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import text

Base = declarative_base()


db_url = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}/usersDB"


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    
# read_user function

def read_user(event, context):
    # Parse input data from the event
    user_id = event['pathParameters']['id']

    # Create an SQLAlchemy engine
    db_url = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}/usersDB"
    engine = create_engine(db_url)
    try:
        # Create a session
        Session = sessionmaker(bind=engine)
        session = Session()

        # Execute an SQL query using SQLAlchemy
        
        select_query = text("SELECT user_id, username, email, password FROM users WHERE user_id = :user_id")
        # select_query = text("SELECT user_id, username, email, password FROM users WHERE user_id = 10")
        result = session.execute(select_query, {'user_id': user_id})
        # result = session.execute(select_query)

        # Fetch the user data
        user_data = result.fetchone()

        # Close the session
        session.close()

        if user_data:
            user = {
                'id': user_data.user_id,
                'username': user_data.username,
                'email': user_data.email
            }
            print(user_data)
            return {
                'statusCode': 200,
                'body': json.dumps(user)
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps('User not found')
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }


# create_user function
def create_user(event, context):
    user_data = event['body']
    engine = create_engine(db_url)
    
    try:
        # Create a session
        Session = sessionmaker(bind=engine)
        session = Session()
        
        new_user = User(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        
        session.add(new_user)
        
        session.commit()
        
        session.close()
        
        return {
            'statusCode': 200,
            'body': json.dumps('User Created Successfully')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
        
        
# update_user

def update_user(event,context):
    user_id = event['pathParameters']['id']
    user_data = event['body']
    
    engine = create_engine(db_url)
    
    try:
        # Create a session
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Retrieve the user to update
        user_to_update = session.query(User).filter_by(user_id=user_id).first()
        
        if user_to_update:
            user_to_update.username = user_data['username']
            user_to_update.email = user_data['email']
            
            session.commit()
            
            session.close()
            
            return {
                'statusCode':200,
                'body': json.dumps("User updated successfully")
            }
        else:
            return {
                'statusCode': 404,
                'body':json.dumps('User not found')
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
    
# delete_user

def delete_user(event, context):
    user_id = event['pathParameters']['id']
    
    engine = create_engine(db_url)
    
    try:
        # Create a session
        Session = sessionmaker(bind=engine)
        session = Session()
        
        delete_query = text('DELETE FROM users WHERE user_id=:user_id')
        session.execute(delete_query,{'user_id': user_id})
        
        session.commit()
        
        return {
            'statusCode':200,
            'body': json.dumps('User deleted successfully')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
    
    