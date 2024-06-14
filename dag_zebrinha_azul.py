import json
from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import DagRun
from airflow.operators.http_operator import SimpleHttpOperator


default_args = {
    "owner": "Artificial Intelligence",
    "depends_on_past": False,
    "start_date": datetime(2022, 11, 14, 00, 00),
    "email_on_failure": False,
    "email_on_retry": False,
    "provide_context": True
}

execute_date = datetime.now() - timedelta(hours=3)
execution_date = execute_date.strftime("%Y-%m-%d %H:%M")

dag = DAG(
    dag_id="zebrinha-azul", default_args=default_args, start_date=datetime(2022, 11, 14), schedule_interval=timedelta(hours=1), catchup=False, max_active_runs=1
)

raw_post = SimpleHttpOperator(
    task_id="raw",
    endpoint="/v1/raw",
    method="POST",
    data=json.dumps({"execution_date": execution_date}),
    response_check=lambda response: json.loads(response.text),
    log_response=True,
    retries=3,
    retry_delay=timedelta(minutes=5),
    dag=dag,
)


application_post = SimpleHttpOperator(
    task_id="application",
    endpoint="/v1/application",
    method="POST",
    data=json.dumps({"execution_date": execution_date}),
    response_check=lambda response: json.loads(response.text),
    log_response=True,
    retries=3,
    retry_delay=timedelta(minutes=5),
    dag=dag,
)

raw_post >> application_post

DAGS = [dag]
