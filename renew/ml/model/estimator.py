from renew.exception import SolarException
import os,sys
from renew.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME



class RenewModel:

    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise SolarException(e,sys)
        

    def predict(self,x):
        try:
            x_transform = self.preprocessor.fit_transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise SolarException(e,sys)
        


class ModelResolver:
    def __init__(self,model_dir = SAVED_MODEL_DIR):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise SolarException(e,sys)
    

    def get_letest_model_path(self,)->str:
        try:
            timestamps = list(map(int,os.listdir(self.model_dir)))
            latest_timestamp = max(timestamps)
            latest_model_path = os.path.join(self.model_dir,f"{latest_timestamp}",MODEL_FILE_NAME)
            return latest_model_path
        except Exception as e:
            raise SolarException(e,sys)
    

    def is_model_exist(self,):
        try:
             if not os.path.exists(self.model_dir):
                return False

             timestamps = os.listdir(self.model_dir)
             if len(timestamps)==0:
                return False
            
             latest_model_path = self.get_letest_model_path()

             if not os.path.exists(latest_model_path):
                return False

             return True
        except Exception as e:
            raise SolarException(e,sys)
