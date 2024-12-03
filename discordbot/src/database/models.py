from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

# Create a table to store discord user id and the user token
class UserToken(Base):
    __tablename__ = 'userid_token'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(64), unique=True, nullable=False)
    token = Column(String(200), unique=True, nullable=False)
    
    
# Create a table to store discord server id and the server prefix
class ServerPrefix(Base):
    __tablename__ = 'serverid_prefix'
    id = Column(Integer, primary_key=True, index=True)
    server_id = Column(String(64), unique=True, nullable=False)
    prefix = Column(String(5), nullable=False)