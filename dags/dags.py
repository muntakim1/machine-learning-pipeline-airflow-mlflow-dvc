from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.sensors.filesystem import FileSensor

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='training',
    default_args=default_args,
    schedule_interval="* * * * *",
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:
    param_changes = FileSensor(
        task_id='monitor_change_in_params',
        filepath="/home/muntakim/CustomerSegmentation/params.yaml",
        poke_interval=5,  # check every 60 seconds
        timeout=60 # timeout after 10 minutes
    )
    file_change = FileSensor(
        task_id='monitor_change_in_train_csv',
        filepath="/home/muntakim/CustomerSegmentation/data/processed/train.csv",
        poke_interval=5,  # check every 60 seconds
        timeout=60 # timeout after 10 minutes
    )
    trigger = BashOperator(
        task_id='dvc_stater',
        bash_command="cd ~/CustomerSegmentation/ && ~/CustomerSegmentation/.venv/bin/dvc repro"
    )
    param_changes >> trigger
    file_change >> trigger