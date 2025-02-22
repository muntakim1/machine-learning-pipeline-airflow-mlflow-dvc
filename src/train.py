import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score,calinski_harabasz_score,davies_bouldin_score
import json
import yaml
import mlflow 
from utils.logger import logger
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
with open('params.yaml','r') as f:	
    config=yaml.safe_load(f)

with open('hyperparameter_config.json','r') as f:
    params=json.load(f)

mlflow.set_tracking_uri("http://localhost:5000")


df=pd.read_csv(config['training_params']['training_path'])
scaler = StandardScaler()
columns_to_exclude = ['CustomerID']
columns_to_scale = df.columns.difference(columns_to_exclude)
df_scaled=df.copy()
# Scale the data
df_scaled[columns_to_scale] = scaler.fit_transform(df_scaled[columns_to_scale])

n_clusters=params['n_clusters']
# Read the data

km = KMeans(n_clusters=n_clusters,init=config['training_params']['init'], n_init=config['training_params']['n_init'], max_iter=config['training_params']['max_iter'], random_state=config['training_params']['random_state'])

df['cluster']=km.fit_predict(df_scaled)

# Calculate Silhouette Score
silhouette_avg = silhouette_score(df_scaled, df['cluster'])
logger.info(f"Silhouette Score: {silhouette_avg:.3f}")

# Calculate Calinski-Harabasz Score
calinski_harabasz = calinski_harabasz_score(df_scaled, df['cluster'])
logger.info(f"Calinski-Harabasz Score: {calinski_harabasz:.3f}")

# Calculate Davies-Bouldin Score
davies_bouldin = davies_bouldin_score(df_scaled, df['cluster'])
logger.info(f"Davies-Bouldin Score: {davies_bouldin:.3f}")


metrics={'silhouette': silhouette_avg, 'calinski-harabasz': calinski_harabasz, 'davies-bouldin': davies_bouldin}
training_dict={
    'n_cluster':n_clusters,
    'n_init':config['training_params']['n_init'],
    'max_iter':config['training_params']['max_iter'],
    'random_state':config['training_params']['random_state']
    }
grouped_data = df.groupby(by='cluster')['CustomerID'].count()
grouped_data.plot(kind='bar', color='midnightblue')
plt.savefig('cluster.png')

with mlflow.start_run():
    # Log metrics
    mlflow.log_metrics(metrics)
    mlflow.log_params(training_dict)
    mlflow.log_artifact("ELBOW_FOR_CLUSTER.png")
    mlflow.log_artifact("cluster.png")
    # Log the model
    mlflow.sklearn.log_model(km, "kmeans_model")


with open('reports/metrics.json','w') as f:
    json.dump(metrics, f)
