import pandas as pd
import os
import sys
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler,MinMaxScaler
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.logger import logger

logger.info("Feature Extraction started.")
df=pd.read_csv('data/preprocessed/processed_data.csv')
df['InvoiceDate']=pd.to_datetime(df['InvoiceDate'])
logger.info("DataFrame has been loaded")

df['Sales']=df['Quantity']*df['UnitPrice']

logger.info("New Feature Sales created.")

df['CustomerID']=df['CustomerID'].astype(str).str.replace('.0','',regex=False)
logger.info("CustomerID is converted to String.")

customer_df=df.groupby('CustomerID').agg({'InvoiceNo':'nunique','Description':'nunique','Sales':'sum','Quantity':'sum'}).reset_index()
logger.info("New DataFrame customer_df has been created.")

customer_df.rename({'InvoiceNo':'Invoices','Description':'DistinctProducts','Quantity':'OverallQuantity'},axis=1,inplace=True)
logger.info("Renamed some of the columns.")

customer_df['SalesPerInvoice']=round(customer_df['Sales']/customer_df['Invoices'],2)
logger.info("Sales per invoice has been created.")

customer_df['ItemsPerInvoice']=round(customer_df['OverallQuantity']/customer_df['Invoices'],2)
logger.info("Items per invoice has been created.")

customer_df.sort_values('Invoices',inplace=True)

overall_max_date=df['InvoiceDate'].max()

timerange_df=df.groupby('CustomerID').agg(min_date=('InvoiceDate','min'),max_date=('InvoiceDate','max')).reset_index()

timerange_df['DistinctMonths']=((timerange_df['max_date'].dt.year - timerange_df['min_date'].dt.year) * 12 + 
                                  (timerange_df['max_date'].dt.month - timerange_df['min_date'].dt.month))+1
timerange_df['LastBuyMonths']= ((overall_max_date.year - timerange_df['max_date'].dt.year) * 12 + 
                                  (overall_max_date.month - timerange_df['max_date'].dt.month))+1

customer_df=customer_df.merge(timerange_df[['CustomerID','DistinctMonths','LastBuyMonths']],on='CustomerID',how='left')	
logger.info("New Features called DistinctMonths and LastBuyMonths have been created")

customer_df['SalesPerMonth']=round(customer_df['Sales']/customer_df['DistinctMonths'])
logger.info("New Features called SalesPerMonth has been created")

df['WeekDay']= df['InvoiceDate'].dt.weekday

df['is_weekend']=df['InvoiceDate'].dt.weekday >=5

weekend_df=df.groupby('CustomerID').agg(uniqueWeekdayInovices=('InvoiceNo',lambda x:len(x[df['is_weekend']==False].unique())),
                                          uniqueWeekendInovices=('InvoiceNo',lambda x:len(x[df['is_weekend']==True].unique()))).reset_index()
customer_df=pd.merge(customer_df,weekend_df,how='left',on='CustomerID')
logger.info("New Features called is_weekend & WeekDay have been created")
customer_df['WeekendPct']=customer_df['uniqueWeekendInovices']/customer_df['Invoices']
logger.info("New Features called WeekendPct have been created")


scaler = StandardScaler()
columns_to_exclude = ['CustomerID']
columns_to_scale = customer_df.columns.difference(columns_to_exclude)

train,test=train_test_split(customer_df, test_size=0.2)
train.to_csv('data/processed/train.csv')	
test.to_csv('data/processed/test.csv')


logger.info("Train and Test file have been saved")