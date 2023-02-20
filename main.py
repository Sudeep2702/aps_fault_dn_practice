from sensor.logger import logging
from sensor.exception import SensorException
import os,sys
from sensor.utils import get_collecton_dataframe
from sensor.entity import config_entity
from sensor.component.dataingestion import DATA_INGESTION
from sensor.component.data_validation import DATA_VALIDATION
from sensor.component.data_transformation import DataTransformation  
from sensor.component.model_train import ModelTrainer
        
if __name__=="__main__":

   try:
      training_pipeline_config = config_entity.TRAINING_PIPELINE_CONGIF()

      #data ingestion
      data_ingestion_config  = config_entity.DATA_INGESTION_CONFIG(trainingpipeline_config=training_pipeline_config)
      print(data_ingestion_config.to_dic())
      data_ingestion = DATA_INGESTION(data_ingestion_config=data_ingestion_config)
      data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

    #data validation
      data_validation_config = config_entity.DATA_VALIDATION_CONFIG(trainingpipeline_config=training_pipeline_config)
      data_validation = DATA_VALIDATION(data_validation_config=data_validation_config,
                        data_ingestion_artifact=data_ingestion_artifact)

      data_validation_artifact = data_validation.initiate_data_validation()
      

   #data_transformation 
      data_transformation_config  = config_entity.DataTransformationConfig(trainingpipeline_config=training_pipeline_config)
      data_tranformation = DataTransformation(data_transformation_config=data_transformation_config, data_ingestion_artifact=data_ingestion_artifact)
      data_transform_art = data_tranformation.initiate_data_transformation()


   #model_trainer
      
      model_trainerconfig= config_entity.ModelTrainerConfig(trainingpipeline_config=config_entity.TRAINING_PIPELINE_CONGIF())
      MODEL_TRAINER = ModelTrainer(model_trainer_config=model_trainerconfig , data_transformation_artifact= data_transform_art)
      model_trainer_art = MODEL_TRAINER.initiate_model_trainer()




 

      
   except Exception as e:
      raise SensorException(e, sys)
   



     