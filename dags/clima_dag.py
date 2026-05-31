from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="pipeline_clima_sao_luis",
    start_date=datetime(2025, 1, 1),
    schedule="0 15 * * *",
    catchup=False
) as dag:

    executar_pipeline = BashOperator(
        task_id="executar_pipeline",
        bash_command="cd /opt/airflow/project && python src/pipeline.py"
    )