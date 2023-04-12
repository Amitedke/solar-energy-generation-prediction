from renew.configuration.mongo_db_connection import MongodbClient

if __name__ == '__main__':
    mongodb_client = MongodbClient()
    print(mongodb_client.database.list_collection_names())