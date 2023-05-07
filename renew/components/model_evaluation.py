from renew.exception import SolarException
from renew.logger import logging
from renew.entity.config_entity import ModelEvaluationConfig
from renew.entity.artifact_entity import ModelTrainerArtifact,ModelEvaluationArtifact,DataValidationArtifect
from renew.ml.model.estimator import ModelResolver
from renew.utlis.main_utils import save_object,load_object,write_yaml_file,read_data
from renew.constant.training_pipeline import TARGET_COLUMN
import os,sys
import pandas as pd
from renew.ml.score.model_score import get_regression_report
import joblib
import numpy as np

class ModelEveluation:
    def __init__(self, model_eval_config:ModelEvaluationConfig,data_validation_artifect : DataValidationArtifect,model_trainer_artifact : ModelTrainerArtifact):
        try:
            self.model_eval_config = model_eval_config
            self.data_validation_artifect = data_validation_artifect
            self.model_trainer_artifect = model_trainer_artifact
        
        except Exception as e:
            raise SolarException(e,sys)
        



    
    def intiate_model_eveluation(self)->ModelEvaluationArtifact:
        try:
            valid_train_file_path = self.data_validation_artifect.valid_train_file_path
            valid_test_file_path = self.data_validation_artifect.valid_test_file_path

            train_df = read_data(valid_train_file_path)
            test_df = read_data(valid_test_file_path)
            logging.info("train_df and test_df are formed")
            df = pd.concat([train_df, test_df])
            y_true = df[TARGET_COLUMN]
            logging.info("target columns are asigned")
            df.drop(TARGET_COLUMN,axis=1,inplace=True)
            logging.info("target features are droped from main dataframe")
            train_model_file_path = self.model_trainer_artifect.trained_model_file_path
            model_resolver = ModelResolver()
            is_model_accepted = True


            if not model_resolver.is_model_exist():
                model_eveluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted=is_model_accepted,
                    improved_accuracy=None,
                    best_model_path=None,
                    trained_model_path=train_model_file_path,
                    train_model_metric_artifact = self.model_trainer_artifect.test_metric_artifact,
                    best_model_metric_artifact=None
                )
                logging.info(f"model eveluation artifect {model_eveluation_artifact}")
                return model_eveluation_artifact
            

            latest_model_file_path = model_resolver.get_letest_model_path()



            train_model = load_object(file_path = train_model_file_path)
            latest_model  = load_object(file_path = latest_model_file_path)


            
            logging.info("models are loaded")
            
            # y_train_pred = train_model.predict(df)
            # y_latest_pred = latest_model.predict(df)
            # logging.info(f"y preds are formed")


            # trained_score = get_regression_report(y_true=y_true,y_pred=y_train_pred)
            # latest_score = get_regression_report(y_true=y_true,y_pred=y_latest_pred)
            # logging.info(f"reports are created")

            # if trained_score.r2_score > latest_score.r2_score:
            #     is_model_accepted = True
            
            # else:
            #     is_model_accepted = False
            # logging.info(f"dis has been made")
            

            model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted=is_model_accepted, 
                    improved_accuracy=None, 
                    best_model_path=latest_model, 
                    trained_model_path=train_model_file_path, 
                    train_model_metric_artifact=None,  
                    best_model_metric_artifact=None)
            
            logging.info(f"new artifact is formed")
            model_eval_report = model_evaluation_artifact.__dict__

            write_yaml_file(self.model_eval_config.report_file_path,model_eval_report)

            logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact
        
        except Exception as e:
            raise SolarException(e,sys)


        
    


