from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

from airflow import DAG


def _t1(ti):
    ti.xcom_push(key='my_key', value=42)

def _t2(ti):
    var = ti.xcom_pull(key='my_key', task_ids='t1')
    print('Printing my_key:', var)

with DAG(
    dag_id='xcom_dag',
    start_date=datetime(2022, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:
    t1 = PythonOperator(
        task_id='t1',
        python_callable=_t1
    )

    t2 = PythonOperator(
        task_id='t2',
        python_callable=_t2
    )

    t3 = BashOperator(
        task_id='t3',
        bash_command="echo ''"
    )

    t1 >> t2 >> t3
