from sensor.entity import artifact_entity,config_entity
from sensor.exception import SensorException
from sensor.logger import logging
from scipy.stats import ks_2samp
from typing import Optional
import os,sys 
import pandas as pd
from sensor import utils
import numpy as np
import pandas


class DATA_VALIDATION:
    def __init__(self ,data_validation_config:config_entity.DATA_VALIDATION_CONFIG,
                 data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config = data_validation_config
            self.validation_error = dict()
            self.data_ingestion_artifact = data_ingestion_artifact



        except Exception as e:
            raise SensorException(e, sys)



    def drop_missingvalues_columns(self,df:pandas.DataFrame,report_key_name:str)->Optional[pandas.DataFrame]:
        """
        this function will drop the columns which contains more missing values more than threshold
        df : accpts pandas as dataframe
        threshold:percentage criteria to drop a column
        =========================================================
        returns Pandas Dataframe if atleasr single column is available after missing value cloumns are dropped
        """
        try:

            threshold = self.data_validation_config.missing_treshold
            #selscting columns which contains null values
            null_report = df.isna().sum()/df.shape[0]
             #dropping the columns which contains null
            logging.info(f"selecting column name which contains null above to {threshold}")
            drop_columns_names = null_report[null_report>threshold].index
            logging.info(f"Columns to drop: {list(drop_columns_names)}")
            self.validation_error[report_key_name]=drop_columns_names
            df.drop(list(drop_columns_names),axis=1,inplace=True)
            # return none if no columns left
            if len(df.columns)==0:
                return None

        except Exception as e :
            raise SensorException(e, sys)

    def required_columns_exists(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str)->bool:

        try:
            
            base_columns = base_df.columns
            current_columns = current_df.columns
            missing_columns = []
           
            for base_column in base_columns:
                if base_column not in current_columns:
                    missing_columns.append(base_column)
            if len(missing_columns)>0:
                self.validation_error["missing_columns"]= missing_columns
                return False
            return True
        
    
        
        except Exception as e:
            raise SensorException(e, sys)
    




            

        try :
            def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str):

                drift_report = dict()
                base_columns = base_df.columns
                current_columns = current_df.columns
                for base_column in base_columns :


                    base_data,current_data = base_df[base_column],current_df[current_column]
                    same_dist = s_2samp(base_data,current_data)

                    if same_dist.pvalue>0.05:
                    #we are accepting the null hypothesis
                        drift_report[base_column]= {"p_values":same_dist.pvalue,"same_dist":True}
                    #same distribution 
                    else :
                        drift_report[base_column]={"pvalues":same_dist.pvalue,"same_dist":False}
                        #different distribution

                self.validation_error[report_key_name]
        except Exception as e:
            raise SensorException(e, sys)

            





    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact():
        try:
            logging.info(f"Reading base dataframe")
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            base_df.replace({"na":np.NAN},inplace=True  )
            logging.info(f"Replace na value in base df")
            #basedf has null
            logging.info(f"Drop null values colums from base df")
            base_df = self.drop_missingvalues_columns(df=base_df,report_key_name = "missing_values_within_the_dataset")
            logging.info(f"Reading train dataframe")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info(f"Reading test dataframe")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            logging.info(f"Drop null values colums from train df")
            train_df=self.drop_missingvalues_columns(df=train_df,report_key_name="missing_values_in_base_train_datset") 
            logging.info(f"Drop null values colums from test df")
            test_df=self.drop_missingvalues_columns(df=test_df,report_key_name="missing_values_in_base_test_datset") 
            
            logging.info(f"Is all required columns present in train df")
            train_df_status =  self.required_columns_exists(base_df= base_df,current_df=train_df,report_key_name="missingcolumn_in_train_data_set")
            logging.info(f"Is all required columns present in testdf")
            test_df_status =   self.required_columns_exists(base_df=base_df, current_df=test_df,report_key_name="missingcolumn_in_test_data_set")

            if train_df_status:
                logging.info(f"As all column are available in train df hence detecting data drift")
                self.data_drift(base_df=base_df,current_df=train_df,report_key_name="data_drift_in_train_data_set")
            if test_df_status:
                logging.info(f"As all column are available in test df hence detecting data drift")
                self.data_drift(base_df=base_df,current_df= test_df,report_key_name="data_drift_in_train_data_set")

            #write the report
            
            logging.info("Write reprt in yaml file")
            utils.write_yaml_file(file_path= self.data_validation_config.report_file_path, data= self.validation_error)

            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path)
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        
        
        
        except Exception as e:
            raise SensorException(e, sys)
                