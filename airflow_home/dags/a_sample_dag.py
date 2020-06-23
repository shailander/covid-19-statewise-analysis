#Importing modules
from datetime import timedelta
import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import date
import os

from etl_tasks import *

today_str = date.today().strftime("%Y-%d-%m")

#Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(0),
    # 'email': ['airflow@example.com'],
    # 'email_on_failure': False,
    # 'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

#Instantiate a DAG
dag = DAG(
    'covid_data_dag', default_args=default_args,
    schedule_interval="@daily")

def upload():
    cmd = f"sqoop export   --table covid_data  --connect 'jdbc:mysql://localhost:3306/test'   --username root   --password 123Nineleap   --export-dir 'covid_data.csv'"
    os.system(cmd)
    print(cmd)

#Task1
get_data_upload_hdfs_operator = PythonOperator(task_id='get_covid_data_upload_hdfs_task',
                                   python_callable=get_data,
                                   provide_context=True,
                                   dag=dag)

#Task2
upload_data_to_hive_operator = PythonOperator(task_id='upload_data_hive_task',
                                      python_callable=upload_data_to_hive,
                                      provide_context=True,
                                      dag=dag)

#Task3
connect_mysql_operator = PythonOperator(task_id="connect_mysql_task",
                                        python_callable=create_mysql,
                                        provide_context=True,
                                        dag=dag)

#Task4
sql_upload_operator = PythonOperator(task_id="upload_data_mysql_task",
                                        python_callable=upload,
                                        dag=dag)

#Setting up dependencies
get_data_upload_hdfs_operator >> upload_data_to_hive_operator >> connect_mysql_operator >> sql_upload_operator