# -*- coding: utf-8 -*-
import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import timedelta

default_args = {
    'owner': '4change',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(2),
    'email': ['4change@qq.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'adhoc':False,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'trigger_rule': u'all_success'
}


def print_hello():
    return 'Hello world!'


dag = DAG('hello_world_dag', default_args=default_args, description='hello world dag', schedule_interval=timedelta(days=1))

date_operator = BashOperator(task_id='date_task', bash_command='date', dag=dag)
sleep_operator = BashOperator(task_id='sleep_task', depends_on_past=False, bash_command='sleep 5', dag=dag)
hello_operator = PythonOperator(task_id='hello_task', python_callable=print_hello, dag=dag)

# 设置各任务间的依赖关系
sleep_operator.set_upstream(date_operator)
hello_operator.set_upstream(date_operator)
