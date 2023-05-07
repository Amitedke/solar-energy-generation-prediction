from renew.exception import SolarException
from renew.logger import logging
from renew.entity.config_entity import ModelPusherConfig
from renew.entity.artifact_entity import ModelEvaluationArtifact,ModelPusherArtifact
import os,sys
from renew.utlis.main_utils import save_object,load_object,write_yaml_file
import shutil



class ModelPusher:
    def __init__(self,model_pusher_config : ModelPusherConfig,model_evaluation_artifact: ModelEvaluationArtifact):
        try:
            self.model_pusher_config = model_pusher_config
            self.model_evaluation_artifact = model_evaluation_artifact
        except Exception as e:
            raise SolarException(e,sys)
    


    def intiate_model_pusher(self,)-> ModelPusherArtifact:
        try:
            trained_model_path = self.model_evaluation_artifact.trained_model_path
            model_file_path = self.model_pusher_config.model_file_path
            os.makedirs(os.path.dirname(model_file_path),exist_ok=True)
            shutil.copy(src=trained_model_path,dst=model_file_path)
            logging.info("dir created for model pusher 11")

            save_model_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(save_model_path),exist_ok=True)
            shutil.copy(src=trained_model_path,dst=save_model_path)
            logging.info("dir created for model pusher 22")

            model_eveluation_artifact = ModelPusherArtifact(saved_model_path=save_model_path,model_file_path=model_file_path)

            return model_eveluation_artifact
        except Exception as e:
            raise SolarException(e,sys)


            

        except Exception as e:
            raise SolarException(e,sys)

