
from renew.data_access.renew_data import RenewData
import pandas as pd
import os
from renew.utlis.main_utils import save_csv_file
from renew.constant.pipeline import FEATURE_STORE,RAW_DATA
from renew.components.data_ingestion import DataIngestion
from renew.pipeline.training_pipeline import TrainingPipeline

if __name__ == "__main__":
    obj = TrainingPipeline()
    obj.run_pipeline()

