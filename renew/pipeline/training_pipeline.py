from renew.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig
from renew.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifect
from renew.exception import SolarException
from renew.components.data_ingestion import DataIngestion
from renew.components.data_validation import DataValidation
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
        
    
    def run_pipeline(self):
        is_pipeline_running = True
        data_ingestion_artifect : DataIngestionArtifact = self.start_data_ingestion()
        data_validation_artifect : DataValidationArtifect = self.start_data_validation(data_ingestion_artifect=data_ingestion_artifect)



        