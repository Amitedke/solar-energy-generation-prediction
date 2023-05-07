import pandas as pd
import numpy as np
import os
import sys
import dill

import yaml
from renew.exception import SolarException

def save_csv_file(data:pd.DataFrame,file_path:str,file_name:str):
    if not os.path.exists(file_path):
        os.makedirs((file_path),exist_ok=True)
        csv_file_path = os.path.join(file_path,file_name)
        data.to_csv(csv_file_path,index=False)

def read_yaml_file(file_path: str):
    try:
        with open(file_path,'rb') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise SolarException(e,sys)
    

def save_dataframes(df1:pd.DataFrame,df2:pd.DataFrame,file_path1:str,file_path2:str,file_name1:str,file_name2:str):
    if not os.path.exists(file_path1) and not os.path.exists(file_path2):
        os.makedirs((file_path1),exist_ok=True)
        os.makedirs((file_path2),exist_ok=True)
        csv_1 = os.path.join(file_path1,file_name1)
        csv_2 = os.path.join(file_path2,file_name2)
        df1.to_csv(csv_1,index=False)
        df2.to_csv(csv_2,index=False)


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise SolarException(e, sys)
    

def read_data(file_path: str)-> pd.DataFrame:
    df = pd.read_csv(file_path)
    return df



def save_numpy_array_data(file_path: str, array:np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open (file_path, 'wb') as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        SolarException(e,sys)


def load_numpy_array_data(file_path: str):
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        SolarException(e,sys)




def save_object(file_path: str, obj: object) -> None:
    try:
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise SolarException(e, sys) from e


def load_object(file_path: str, ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise SolarException(e, sys) from e