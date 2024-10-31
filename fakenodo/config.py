# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    FAKENODO_API_URL = "http://localhost:5001/api/fakenodo"
    WORKING_DIR = os.getenv("WORKING_DIR", "/tmp")
    UPLOADS_FOLDER_NAME = os.getenv("UPLOADS_FOLDER_NAME", "uploads")
