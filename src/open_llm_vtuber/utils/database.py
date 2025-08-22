from pymongo import MongoClient
from loguru import logger

class MongoDBManager:
    def __init__(self, connection_string: str, db_name: str = "ai_interviewer_db"):
        self.client = None
        self.db = None
        try:
            self.client = MongoClient(connection_string)
            self.db = self.client[db_name]
            logger.info(f"Successfully connected to MongoDB database: {db_name}")
        except Exception as e:
            logger.error(f"Could not connect to MongoDB: {e}")
            self.client = None
            self.db = None

    def save_message(self, collection_name: str, message: dict):
        if not self.db:
            logger.warning("MongoDB not connected. Message not saved.")
            return
        try:
            collection = self.db[collection_name]
            result = collection.insert_one(message)
            logger.info(f"Message saved to MongoDB with ID: {result.inserted_id}")
        except Exception as e:
            logger.error(f"Error saving message to MongoDB: {e}")

    def close_connection(self):
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed.")

# Global instance (will be initialized with connection string from config)
mongo_manager = None

def initialize_mongodb(connection_string: str, db_name: str = "ai_interviewer_db"):
    global mongo_manager
    mongo_manager = MongoDBManager(connection_string, db_name)
