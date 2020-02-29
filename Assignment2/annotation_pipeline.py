from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
#import processing


default_args = {
	'owner': 'team2',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'catchup': False,
    'email': ['sharvari.karnik25@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}


dag = DAG('annotation',default_args=default_args,schedule_interval=None,max_active_runs=1)


t0 = BashOperator(
    task_id='Install1',
    bash_command='pip install --user nltk',
    dag=dag)
t1 = BashOperator(
    task_id='Install2',
    bash_command='pip install --user boto3',
    dag=dag)
t2 = BashOperator(
    task_id='Scrape',
    bash_command='pip install --user ibm-watson',
    dag=dag)

t3 = BashOperator(
    task_id='IBM_API',
    bash_command='python /mnt/c/dag/processing.py',
    dag=dag)

t0 >> t1 >> t2 >> t3