from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from datetime import datetime

from airflow import DAG
import random

def _t1(ti):
    ti.xcom_push(key='random_value', value=random.randint(0, 100))
    print('Running t1...')

def _t2(ti):
    ti.xcom_pull(key='random_value', task_ids='t1')
    print('Value smaller than 50...')

def _branch(ti):
    value = ti.xcom_pull(key='random_value', task_ids='t1')
    if value < 50:
        return 't2'
    return 't3'


with DAG(
    dag_id='branch_operator_demo',
    start_date=datetime(2022, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:
    t1 = PythonOperator(
        task_id='t1',
        python_callable=_t1
    )

    branch = BranchPythonOperator(
        task_id='branch',
        python_callable=_branch
    )

    t2 = PythonOperator(
        task_id='t2',
        python_callable=_t2
    )

    t3 = BashOperator(
        task_id='t3',
        bash_command="echo 'Value greater or equal than 50...'"
    )

    t1 >> branch >> [t2, t3]
