import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.logger import logger

df=pd.read_csv('data/raw/data.csv',encoding='unicode_escape')
logger.info('Data has been loaded to dataframe.')

nan_count = df.isna().sum()
logger.info(f'Number of NaNs in each column: {nan_count}')
df.dropna(subset=['CustomerID','Description'],inplace=True)
logger.info('Nans have been dropped.')

duplicate_count = df.duplicated().sum()
logger.info(f'Number of duplicate rows: {duplicate_count}')
df.drop_duplicates(inplace=True)
logger.info('Duplicates have been dropped.')

quantity_issues = df[df['Quantity'] <= 0]
logger.info(f'Number of rows with Invalid quanity: {len(quantity_issues)}')
df=df[df['Quantity']>0]
logger.info('Invalid quanity have been dropped.')

unitprice_issues=df[df['UnitPrice'] <= 0]
logger.info(f'Number of rows with Invalid unit price: {len(unitprice_issues)}')
df=df[df['UnitPrice']>0]
logger.info("Invali unit price have been dropped.")

pct_98_quantity=df['Quantity'].quantile(0.98)
pct_98_unitprice=df['UnitPrice'].quantile(0.98)
logger.info(f"Quantity and UnitPrice 98th percentiles. {pct_98_quantity} & {pct_98_unitprice}")

removed_outliers=df[(df['Quantity']<pct_98_quantity) &(df['UnitPrice']<pct_98_unitprice)]
logger.info("Outliers have been removed.")


removed_outliers.to_csv('data/preprocessed/processed_data.csv')