from renew.entity.artifact_entity import DataValidationArtifect,DataTransformationArtifact,DataIngestionArtifact
from renew.utlis.main_utils import save_csv_file,save_dataframes,load_numpy_array_data,read_yaml_file,write_yaml_file,read_data,save_numpy_array_data,save_object,load_object
from renew.logger import logging
from renew.exception import SolarException
from renew.entity.config_entity import DataTransformationConfig
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
import os,sys
from renew.constant.training_pipeline import TARGET_COLUMN

class DataTransformation:
    def __init__(self,data_validation_artifact : DataIngestionArtifact,data_transformation_config : DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise SolarException(e,sys)
    


    def get_data_transformer_object(cls)->Pipeline:
        try:
            standred_scalar = StandardScaler()
            processor = Pipeline(
                steps=["standred_scalar",standred_scalar]
            )
        
            return processor
        except Exception as e:
            raise SolarException(e,sys)
    

    def intiate_data_transformation(self,)->DataTransformationArtifact:
        try:
            train_df : pd.DataFrame = read_data(self.data_validation_artifact.trained_file_path)
            test_df : pd.DataFrame = read_data(self.data_validation_artifact.test_file_path)
            target_feature_train_df = train_df[TARGET_COLUMN].to_numpy()
            target_feature_test_df = test_df[TARGET_COLUMN].to_numpy()
            logging.info("target feature created separate")
            preprocessor = self.get_data_transformer_object()
            train_df_droped = train_df.drop(TARGET_COLUMN,axis=1)
            test_df_droped = test_df.drop(TARGET_COLUMN,axis=1)
            logging.info("dependend varibles are dropped")
            train_df_droped['Timestamp'] = pd.to_datetime(train_df_droped['Timestamp'])
            test_df_droped['Timestamp'] = pd.to_datetime(test_df_droped['Timestamp'])
            train_df_droped['Month'] = train_df_droped['Timestamp'].dt.month
            test_df_droped['Month'] = test_df_droped['Timestamp'].dt.month
            logging.info("Month feature is added")
            train_df_droped = train_df_droped.drop(['Timestamp'],axis = 1)
            test_df_droped = test_df_droped.drop(['Timestamp'],axis = 1)
            logging.info("timestamp is dropped")
            preprocessor_object_train = None
            sc = StandardScaler()
            transform_input_train_frature =sc.fit_transform(train_df_droped)
            transform_input_test_frature = sc.fit_transform(test_df_droped)
            logging.info("values are transformed")
          #  target_feature_train_df_1 = np.array(target_feature_train_df)
           # target_feature_test_df_1 = np.array(target_feature_test_df)
            logging.info("outputs converted into arrays")
            train_arr = np.c_[transform_input_train_frature,target_feature_train_df]
            test_arr = np.c_[transform_input_test_frature,target_feature_test_df]
            logging.info("arrays are formed")
           # train_array_new = np.concatenate((train_arr,target_feature_train_df_1))
           # test_array_new = np.concatenate((test_arr,target_feature_test_df_1))
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object_train)


            data_transformation_artifact = DataTransformationArtifact (transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                                                                       transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                                                                       transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,)
            

            return data_transformation_artifact
        except Exception as e:
            raise SolarException(e,sys)    

















        




        
    
        


