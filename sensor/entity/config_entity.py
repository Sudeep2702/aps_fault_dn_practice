from sensor.exception import SensorException
from sensor.logger import logging
import pandas as pd 
import numpy as np 
import sys , os
from datetime import datetime
FILE_NAME = "sensor.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
TRANSFORMER_OBJECT_FILE_NAME = "transformer.pkl"
TARGET_ENCODER_OBJECT_FILE_NAME = "target_encoder.pkl"
MODEL_FILE_NAME = "model.pkl"
class TRAINING_PIPELINE_CONGIF:
    def __init__(self):
        try :
            self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")

        except Exception as e :
            raise SensorException(e, sys)

class DATA_INGESTION_CONFIG:
    def __init__(self,trainingpipeline_config :TRAINING_PIPELINE_CONGIF):
        try: 
            self.database_name = "aps"
            self.collection_name = "sensor"
            self.data_ingestion_dir = os.path.join(trainingpipeline_config.artifact_dir,"data_ingestion")
            self.feature_store_file_path = os.path.join(self.data_ingestion_dir,"feature_store",FILE_NAME)
            self.train_file_path = os.path.join(self.data_ingestion_dir,"dataset",TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.data_ingestion_dir,"dataset",TEST_FILE_NAME)
            self.testsize = 0.2
        except Exception as e:
            return SensorException(e, sys)


    def to_dic(self,)->dict:
        try:
            return self.__dict__
        except Exception  as e:
            raise SensorException(e,sys)     


class DATA_VALIDATION_CONFIG:


    def __init__(self,trainingpipeline_config :TRAINING_PIPELINE_CONGIF):
    
        self.data_validation_dir = os.path.join(trainingpipeline_config.artifact_dir,"data_validation")
        self.report_file_path = os.path.join(self.data_validation_dir,"report.yaml")
        self.missing_threshold:float = 0.7
        self.base_file_path = os.path.join("/config/workspace/aps_failure_training_set1.csv")

       
class DataTransformationConfig:

    def __init__(self,trainingpipeline_config:TRAINING_PIPELINE_CONGIF):
        self.data_transformation_dir = os.path.join(trainingpipeline_config.artifact_dir , "data_transformation")
        self.transform_object_path = os.path.join(self.data_transformation_dir,"transformer",TRANSFORMER_OBJECT_FILE_NAME)
        self.transformed_train_path =  os.path.join(self.data_transformation_dir,"transformed",TRAIN_FILE_NAME.replace("csv","npz"))
        self.transformed_test_path =os.path.join(self.data_transformation_dir,"transformed",TEST_FILE_NAME.replace("csv","npz"))
        self.target_encoder_path = os.path.join(self.data_transformation_dir,"target_encoder",TARGET_ENCODER_OBJECT_FILE_NAME)

class ModelTrainerConfig:

    def __init__(self,trainingpipeline_config:TRAINING_PIPELINE_CONGIF):
        self.model_trainer_dir = os.path.join(trainingpipeline_config.artifact_dir , "model_trainer")
        self.model_path = os.path.join(self.model_trainer_dir,"model",MODEL_FILE_NAME)
        self.expected_score = 0.7
        self.overfitting_threshold = 0.1

