import os
from pymongo import MongoClient
from dotenv import load_dotenv

class MongoConnection:
    def __init__(self):
        load_dotenv()
        db_host = os.getenv("MONGO_HOST")
        db_name = os.getenv("MONGO_DB")
        
        self.client = MongoClient(db_host)
        self.db = self.client[db_name]

    def get_db(self):
        return self.db
