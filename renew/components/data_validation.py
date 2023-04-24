from distutils import dir_util
from renew.constant.training_pipeline import SCHEMA_FILE_PATH
from renew.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifect
from renew.entity.config_entity import DataValidationConfig,TrainingPipelineConfig
from renew.exception import SolarException
from renew.logger import logging
from renew.utlis.main_utils import read_yaml_file,write_yaml_file,read_data
import pandas as pd
from scipy.stats import ks_2samp
import sys,os


class DataValidation:
    def __init__(self,data_ingestion_artifact : DataIngestionArtifact,data_validation_config : DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise Exception(e,sys)
    


    def validate_number_of_columns(self,dataframe : pd.DataFrame)-> bool :
        try:
            number_of_columns = len(self.schema_config["columns"])
            logging.info(f"requird number of columns {number_of_columns}")
            if len(dataframe.columns)==number_of_columns:
              return True
            else:
                return False
        except Exception as e:
            raise SolarException(e,sys)
        
    def is_data_drifted(df1:pd.DataFrame,df2:pd.DataFrame,threshold:float = 0.5)->bool:
        try:
            c1 = df1["Clearsky DHI"]
            c2 = df2["Clearsky GHI"]
            if ks_2samp[df1,df2][0]< threshold:
                return True
            else:
                False
        except Exception as e:
            raise SolarException(e,sys)
        
    def intiate_data_validation(self)->DataValidationArtifect:
        try:
            training_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            train_df = read_data(training_file_path)
            test_df = read_data(test_file_path)
            cond1 = self.validate_number_of_columns(dataframe=train_df)
            #cond2 = self.is_data_drifted(df1 = train_df,df2=test_df)
            self.data_ingestion_artifact

            status = cond1
            data_validation_artifect = DataValidationArtifect(validation_status=status,valid_train_file_path=self.data_ingestion_artifact.trained_file_path,valid_test_file_path=self.data_ingestion_artifact.test_file_path,invalid_train_file_path=None,invalid_test_file_path=None,drift_report_file_path=None)
            logging.info("Data validation artifact created")

            return data_validation_artifect
        except Exception as e:
            raise SolarException(e,sys)

            

        



    

    
        