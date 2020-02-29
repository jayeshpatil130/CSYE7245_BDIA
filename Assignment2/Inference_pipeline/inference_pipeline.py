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


dag = DAG('inference',default_args=default_args,schedule_interval=None,max_active_runs=1)


t0 = BashOperator(
    task_id='scrapy_install',
    bash_command='pip install --user scrapy',
    dag=dag)
t1 = BashOperator(
    task_id='slugify_install',
    bash_command='pip install --user slugify',
    dag=dag)
t2 = BashOperator(
    task_id='boto',
    bash_command='pip install --user boto3',
    dag=dag)

t3 = BashOperator(
    task_id='scrape',
    bash_command='python /mnt/c/dag/scrape_part4.py',
    dag=dag)
	
t4 = BashOperator(
    task_id='api_call',
    bash_command='python /mnt/c/dag/create_json.py',
    dag=dag)

t0 >> t1 >> t2 >> t3 >> t4