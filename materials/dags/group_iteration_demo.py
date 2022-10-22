from airflow import DAG
from airflow.operators.bash import BashOperator

from datetime import datetime


with DAG(
    dag_id='group_iteration_demo',
    start_date=datetime(2022, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:
    check_files = BashOperator(
        task_id='check_files',
        bash_command='sleep 10'
    )

    for i in range(3):
        download_task = BashOperator(
            task_id='download_'+str(i),
            bash_command='sleep 10'
        )

        download_task >> check_files

        transform_task = BashOperator(
            task_id='transform_'+str(i),
            bash_command='sleep 10'
        )

        check_files >> transform_task
