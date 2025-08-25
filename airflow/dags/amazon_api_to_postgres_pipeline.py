from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.providers.amazon.aws.operators.s3 import S3CreateBucketOperator, S3ListOperator

with DAG(
    dag_id="amazon_api_to_postgres_pipeline",
    schedule_interval=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
) as dag:
    create_bucket = S3CreateBucketOperator(
        task_id="create_s3_bucket",
        bucket_name="my-bucket",
        aws_conn_id="minio_default",
        trigger_rule="all_done",
    )

    check_bucket = S3ListOperator(
        task_id="check_s3_bucket",
        bucket="my-bucket",
        aws_conn_id="minio_default",
    )

    generate_data = BashOperator(
        task_id="generate_data",
        bash_command="python /opt/airflow/dags/mock_amazon_api.py",
    )

    upload_to_minio = BashOperator(
        task_id="upload_to_minio",
        bash_command="mc alias set myminio http://minio:9000 minioadmin minioadmin && mc cp /tmp/sales_data.json myminio/my-bucket/sales_data.json",
    )

    trigger_load_to_postgres = TriggerDagRunOperator(
        task_id="trigger_load_to_postgres",
        trigger_dag_id="dag_minio_postgres_pipeline_v2",
        wait_for_completion=True,
    )

    check_bucket >> create_bucket
    create_bucket >> generate_data
    generate_data >> upload_to_minio
    upload_to_minio >> trigger_load_to_postgres