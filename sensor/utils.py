import pandas as pd 
import sys , os 
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.config import mongo_clent 
import yaml

def get_collecton_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    try:
        logging.info(f"reading file from database")
        df = pd.DataFrame(list(mongo_clent[database_name][collection_name].find()))
        logging.info("found comlumns : {df.columns}")
        if "_id" in df.columns:
            logging.info(f"dropping the column : _id")
            df = df.drop("_id",axis=1)
        logging.info(f"found columns and rows in df :{df.shape}" )
        return df 
    except Exception as e:
        raise SensorException(e, sys)


def write_yaml_file(file_path,data:dict):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok = True)
        with open(file_path,"w") as file_writer:
            yaml.dump(data,file_writer)


    except Exception as e:
        raise SensorException(e, sys)