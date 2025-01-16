from zipfile import ZipFile
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.logger import logger

if not os.path.exists("data/raw/data.csv"):
    with ZipFile('zip/data.csv.zip','r') as zip:
        zip.extractall("data/raw/") 
        logger.info("Extraction complete.")
else:
    logger.info('data.csv already exists.')