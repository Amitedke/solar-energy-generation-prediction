from renew.utlis.main_utils import load_numpy_array_data,save_object,load_object
from renew.exception import SolarException
from renew.logger import logging
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
import os,sys
from renew.entity.config_entity import ModelTrainerConfig
from renew.entity.artifact_entity import ModelTrainerArtifact,DataTransformationArtifact
from renew.ml.score.model_score import get_regression_report
from renew.ml.model.estimator import RenewModel




class ModelTrainer:
    def __init__(self,model_trainer_config : ModelTrainerConfig,data_transformation_artifact : DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise SolarException(e,sys)
        
    
    def train_model(self,X_train,y_train):
        try:
            reg = MultiOutputRegressor(RandomForestRegressor())
            reg.fit(X_train,y_train)
            return reg
        except Exception as e:
            raise SolarException (e,sys)
    

    def intiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)
            X_train,y_train,X_test,y_test = (
                train_arr[:, :-3],
                train_arr[:, -3:],
                test_arr[:,:-3],
                test_arr[:, -3:]

            )
            logging.info("X_train,y_train formed")


            model = self.train_model(X_train=X_train,y_train=y_train)
            logging.info("model is creatred")
            y_train_pred = model.predict(X_train)

            reg_score = get_regression_report(y_pred=y_train_pred,y_true=y_train)
            if reg_score.r2_score < self.model_trainer_config.excepted_accuracy:
                raise Exception("train model is not providing good accuracy")
            
            y_test_pred = model.predict(X_test)
            reg_score_1 = get_regression_report(y_pred=y_test_pred,y_true=y_test)

            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path)
            logging.info("model dir created")
            renew_model = RenewModel(preprocessor= preprocessor,model=model)
            save_object(file_path=self.model_trainer_config.trained_model_file_path,obj=renew_model)
            logging.info("object saved")



            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                                          train_metric_artifact=reg_score,
                                                          test_metric_artifact=reg_score_1)
            
            return model_trainer_artifact



















            
            
        
        except Exception as e:
            raise SolarException (e,sys)
        
           

        
    