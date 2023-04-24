from renew.configuration.mongo_db_connection import MongodbClient
from renew.constant.database import DATABASE_NAME,COLLECTION_NAME
from renew.constant.env_variable import MONGODB_URL_KEY
from typing import Optional
import pandas as pd


class RenewData:
    def __init__(self):
        self.database = MongodbClient(database_name=DATABASE_NAME).database
        self.collection = self.database[COLLECTION_NAME]
    

    def export_collection_as_dataframe(self)->pd.DataFrame:
        data = self.collection.find()
        df = pd.DataFrame(data)
        if "_id" in df.columns.to_list():
           df.drop(['_id'],axis=1)
        return df


