from renew.entity.config_entity import DataIngestionConfig
from renew.entity.artifact_entity import DataIngestionArtifact
from renew.utlis.main_utils import read_yaml_file,save_csv_file,save_dataframes
from renew.exception import SolarException
from renew.logger import logging
from renew.data_access.renew_data import RenewData
from renew.constant.training_pipeline import SCHEMA_FILE_PATH
from sklearn.model_selection import train_test_split
import os,sys
import pandas as pd
from pandas import DataFrame

class DataIngestion:
    
    def __init__(self,data_ingection_config : DataIngestionConfig) : 
       try:
       
        self.data_ingection_config = data_ingection_config
        self.schema_file_path = read_yaml_file(SCHEMA_FILE_PATH)
       except Exception as e :
        raise SolarException(e,sys)
       
    def export_data_to_feature_store(self) -> DataFrame:
      try:
        data = RenewData()
        df = data.export_collection_as_dataframe()
        logging.info(f"got data from mongodb and read it as dataframe")
        feature_store_file_path = self.data_ingection_config.feature_store_file_path
        os.path.dirname(feature_store_file_path)
        logging.info(f"feature store dir also created")
        df = DataFrame(df)
        save_csv_file(data=df,file_path=feature_store_file_path,file_name="raw_data.csv")
        logging.info("raw data is stored in feature store")


        return df
      except Exception as e:
        raise SolarException(e,sys)
      

    
    def split_data_as_train_test(self,dataframe : DataFrame)->None:
      try:
        train_set,test_set = train_test_split(dataframe,test_size=self.data_ingection_config.train_test_split_ratio)
        logging.info("split data into train test")
        train_dir_name = os.path.dirname(self.data_ingection_config.training_file_path)
        test_dir_name = os.path.dirname(self.data_ingection_config.test_file_path)
        train_set = pd.DataFrame(train_set)
        test_set = pd.DataFrame(test_set)
        save_dataframes(df1=train_set,df2=test_set,file_path1=train_dir_name,file_path2=test_dir_name,file_name1="train.csv",file_name2="test.csv")
        logging.info("save_dataframes")
        
    
      except Exception as e:
        raise SolarException(e,sys)
      
    
    def intiate_data_ingestion(self)->DataIngestionArtifact:
      try:
        logging.info("presetup")
        dataframe = self.export_data_to_feature_store()
        logging.info("setp")
        dataframe = dataframe.drop(self.schema_file_path["drop_columns"],axis = 1)
        logging.info("columns are dropped")
        self.split_data_as_train_test(dataframe=dataframe)
        data_ingection_artifect = DataIngestionArtifact(trained_file_path=self.data_ingection_config.training_file_path,test_file_path=self.data_ingection_config.test_file_path)

        return data_ingection_artifect
      except Exception as e:
        raise SolarException(e,sys)
    




    

    
    

