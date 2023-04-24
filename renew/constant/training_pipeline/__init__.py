import os
TARGET_COLUMN = "None"
PIPELINE_NAME = "renew"
ARTIFECT_DIR = "artifact"
FILE_NAME = "raw_data.csv"

SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")


TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"


PREPROCESSING_FILE_NAME = "preprocessing.csv" 
MODEL_FILE_NAME = "model.pkl"
SCHEMA_DROP_COLS = "drop_cols"


"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME: str = "solar"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2




"""
Data Validation realted contant start with DATA_VALIDATION VAR NAME
"""

DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"




