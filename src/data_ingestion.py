import os
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml

logger = get_logger(__name__)

class DataIngestion:

    """
        Read all the inputs that needs to run the 
        data ingestion part
    """

    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.bucket_file_name = self.config["bucket_file_name"]
        self.train_ratio = self.config["train_ratio"]

        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info(f"Data ingestion started with {self.bucket_name} and file is {self.bucket_file_name}")

    def download_csv_from_GCP(self):

        """
            Get data from GCP bucket and download it into raw path folder
        """
        
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.bucket_file_name)
            blob.download_to_filename(RAW_FILE_PATH)

            logger.info(f"Raw file is succefully download to {RAW_FILE_PATH}")

        except Exception as e:
            logger.error("Error while downloading the csv file")
            raise CustomException("Failed to download the csv file", e)
        

    def split_the_dataset(self):

        """
            Split the dataset into training and test sets
            Save the training dataset inside the artifacts/raw/{TRAIN_FILE_PATH}
            Save the test dataset inside the artifacts/raw/{TEST_FILE_PATH}
        """

        try:
            logger.info("Starting the splitting process")
            data = pd.read_csv(RAW_FILE_PATH)
            train_data, test_data = train_test_split(data, test_size = 1 - self.train_ratio, random_state = 42)
            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)

            logger.info(f"Files are succufully saved to {TRAIN_FILE_PATH} and {TEST_FILE_PATH}")

        except Exception as e:
            logger.error("Error while splitting the dataset")
            raise CustomException("Failed to split the full file", e)
        
    
    def run(self):

        """
            Read all the functions in a one def function
        """

        try:
            logger.info("Starting data ingestion process")

            self.download_csv_from_GCP()
            self.split_the_dataset()

            logger.info("Data Ingestion is completed")

        except Exception as e:
            logger.error("Error in the data ingestion pipeline")
            raise CustomException("Failed to complete the data ingestion", e)
        
        finally:
            logger.info("Data Ingestion is Completed")

if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()




