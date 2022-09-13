#!/usr/bin/python
# -*- coding: UTF-8 -*-

from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def calculate_ratio_inc(ds, **kwargs):
    # 当前时间(具体到小时), 当前时间加一天(具体到小时)
    current_day_hour = datetime.now().strftime("%Y-%m-%d %H:00:00")
    prev_day_hour = (datetime.now() + timedelta(days=-1)).strftime("%Y-%m-%d %H:00:00")

    sql = '''
        insert into risk_warning_indicator_hourly_report
        select id, risk_indicator_id, hour, value, total, (
                case 
                    when last_total=0 then 0 
                    else (new_total::numeric - last_total::numeric) / last_total::numeric 
                end
            ) as ratio_inc, now()
        from (
            select id, risk_indicator_id, hour, value, total, 
                row_number() over (partition by value order by hour) rn,
                nth_value(total, 1) over (partition by value order by hour) last_total,
                nth_value(total, 2) over (partition by value order by hour) new_total
            from risk_indicator_hourly_report
            where (hour = '$PREV_DAY_HOUR_STR' or hour = '$HOUR_STR')
        ) as tab 
        where tab.rn = 2;
    '''
    sql = sql.replace("$HOUR_STR", current_day_hour)
    sql = sql.replace("$PREV_DAY_HOUR_STR", prev_day_hour)

    engine = create_engine('postgresql://user:password@url:port/db', echo=True, client_encoding='utf8')
    db_session = sessionmaker(bind=engine)
    session = db_session()
    session.execute(sql)
    session.commit()
    session.close()

    return True


default_args = {
    'owner': 'x-graph',
    'depends_on_past': False,
    'start_date': datetime(2019, 3, 24),
    'email': ['x-graph@x-graph.com'],
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

dag = DAG('ratio_inc_dag_1', default_args=default_args, description='ratio_inc dag', schedule_interval='0 * * * *')

ratio_inc_operator = PythonOperator(task_id='ratio_inc_task', provide_context=True, python_callable=calculate_ratio_inc, dag=dag)
