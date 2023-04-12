import pymongo
from renew.constant.database import DATABASE_NAME
from renew.constant.env_variable import MONGODB_URL_KEY
import certifi
import os
ca = certifi.where()

class MongodbClient:
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        if MongodbClient.client is None:
            mongo_db_url = os.getenv(MONGODB_URL_KEY)
            if mongo_db_url is None:
                raise Exception(f"Environment key: {MONGODB_URL_KEY} is not set.")
            MongodbClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
        self.client = MongodbClient.client
        self.database = self.client[database_name]
        self.database_name = database_name
