from renew.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig,ModelEvaluationConfig,ModelPusherConfig
from renew.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifect,DataTransformationArtifact,ModelTrainerArtifact,ModelEvaluationArtifact,ModelPusherArtifact
from renew.exception import SolarException
from renew.components.data_ingestion import DataIngestion
from renew.components.data_validation import DataValidation
from renew.components.data_transformation import DataTransformation
from renew.components.model_trainer import ModelTrainer
from renew.components.model_evaluation import ModelEveluation
from renew.components.model_pusher import ModelPusher
from renew.logger import logging
import os,sys


class TrainingPipeline:
    is_pipeline_running = False
   
   
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            self.data_ingection_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("start data ingestion")
            data_ingestion = DataIngestion(data_ingection_config=self.data_ingection_config)
            data_injection_artifect = data_ingestion.intiate_data_ingestion()

            return data_injection_artifect
        
        except Exception as e:
            raise SolarException(e,sys)
        
    def start_data_validation(self,data_ingestion_artifect : DataIngestionArtifact)->DataValidationArtifect:
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation = DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifect)
            data_validation_artifect = data_validation.intiate_data_validation()
            logging.info("o balle")

            return data_validation_artifect
        except Exception as e:
            raise SolarException(e,sys)
        
    
    def start_data_transformation(self,data_validation_artifact : DataValidationArtifect):
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(data_transformation_config=data_transformation_config,
                                                     data_validation_artifact=data_validation_artifact)
            data_transformation_artifact = data_transformation.intiate_data_transformation()

            return data_transformation_artifact
        except Exception as e:
            raise SolarException(e,sys)
    


    def start_model_trainer(self,data_transformation_artifact : DataTransformationArtifact):
        try:
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,
                                         data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifect = model_trainer.intiate_model_trainer()
            return model_trainer_artifect
        except Exception as e:
            raise SolarException(e,sys)
    

    def start_model_eveluation(self,data_validation_artifact : DataValidationArtifect,
                               model_traier_artiface : ModelTrainerArtifact):
        try:
            model_eval_config = ModelEvaluationConfig(training_pipeline_config=self.training_pipeline_config)
            model_evaluator = ModelEveluation(model_eval_config=model_eval_config,data_validation_artifect=data_validation_artifact,model_trainer_artifact=model_traier_artiface)
            model_eval_artifact = model_evaluator.intiate_model_eveluation()
            return model_eval_artifact
        except Exception as e:
            raise SolarException(e,sys)
    

    def start_model_pusher(self,model_eval_artifect : ModelEvaluationArtifact):
        try:
            model_pusher_config = ModelPusherConfig(training_pipeline_config=self.training_pipeline_config)
            model_pusher = ModelPusher(model_pusher_config=model_pusher_config,model_evaluation_artifact=model_eval_artifect)
            model_pusher_artifact = model_pusher.intiate_model_pusher()
            return model_pusher_artifact
        except Exception as e:
            raise SolarException(e,sys)


        
    
    def run_pipeline(self):
        is_pipeline_running = True
        data_ingestion_artifect : DataIngestionArtifact = self.start_data_ingestion()
        data_validation_artifect : DataValidationArtifect = self.start_data_validation(data_ingestion_artifect=data_ingestion_artifect)
        data_transformation_artifect : DataTransformationArtifact = self.start_data_transformation(data_validation_artifact=data_ingestion_artifect)
        model_trainer_artifect : ModelTrainerArtifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifect)
        model_eval_artifact : ModelEvaluationArtifact = self.start_model_eveluation(data_validation_artifact=data_validation_artifect,model_traier_artiface=model_trainer_artifect)
        model_pusher_artifact : ModelPusherArtifact = self.start_model_pusher(model_eval_artifect=model_eval_artifact)



        