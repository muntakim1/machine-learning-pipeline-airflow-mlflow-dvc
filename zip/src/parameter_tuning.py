import pandas as pd
import yaml
from utils.logger import logger
import seaborn as sns
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer, SilhouetteVisualizer
import matplotlib.pyplot as plt
import json
with open('params.yaml','r') as file:
    config=yaml.safe_load(file)


data=pd.read_csv("data/processed/train.csv")

# Set plot style, and background color
sns.set_theme(style='darkgrid')

# Instantiate the clustering model with the specified parameters
km = KMeans(init=config['cluster_select']['init'], n_init=config['cluster_select']['n_init'], max_iter=config['cluster_select']['max_iter'], random_state=config['cluster_select']['random_state'])

# Create a figure and axis with the desired size
fig, ax = plt.subplots(figsize=(12, 5))

# Instantiate the KElbowVisualizer with the model and range of k values, and disable the timing plot
visualizer = KElbowVisualizer(km, k=tuple(config['cluster_select']['k']), timings=False, ax=ax)

# Fit the data to the visualizer
visualizer.fit(data)

# Finalize and render the figure
visualizer.show('ELBOW_FOR_CLUSTER.png')

with open("hyperparameter_config.json",'w') as file:
    json.dump({'n_clusters': int(visualizer.elbow_value_)},file)