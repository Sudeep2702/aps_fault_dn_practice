from sensor import utils
from sensor.exception import SensorException
from sensor.logger import logging
import os , sys
import pandas as pd 

import numpy as np 
from sensor.entity import config_entity
from sensor.entity import artifact_entity
from sklearn.model_selection import train_test_split

class DATA_INGESTION:
    def __init__(self,data_ingestion_config:config_entity.DATA_INGESTION_CONFIG):
        try :
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        try :
            logging.info(f"exporting colleciton to pd")
            df:pd.DataFrame = utils.get_collecton_dataframe(
                 database_name= self.data_ingestion_config.database_name,
                 collection_name= self.data_ingestion_config.collection_name)
            logging.info("save the data in feature folder")
            
        #replace na with NAN
            df.replace(to_replace= "na",value = np.NAN,inplace = True)


            logging.info("Save data in feature store")

            #replace na with Nan
            df.replace(to_replace="na",value=np.NAN,inplace=True)
            print(df.head())
            #Save data in feature store
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok=True)
            df.to_csv(path_or_buf= self.data_ingestion_config.feature_store_file_path,index = False,header= True)
            #splitting the data
            train_df,test_df = train_test_split(df,test_size=self.data_ingestion_config.testsize)
            

            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok=True)

            train_df.to_csv(path_or_buf = self.data_ingestion_config.train_file_path,index = False , header= True)
            test_df.to_csv(path_or_buf = self.data_ingestion_config.test_file_path,index = False , header= True)

            ##prepare the artifact
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path= self.data_ingestion_config.feature_store_file_path,
                train_file_path= self.data_ingestion_config.train_file_path,
                test_file_path= self.data_ingestion_config.test_file_path)

            return data_ingestion_artifact

        except Exception as e:
            raise SensorException(e, sys)