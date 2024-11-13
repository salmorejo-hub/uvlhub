from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

# Create a table to store discord user id and the user token
class UserToken(Base):
    __tablename__ = 'userid_token'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(64), unique=True, nullable=False)
    token = Column(String(120), unique=True, nullable=False)