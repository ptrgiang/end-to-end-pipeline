from airflow.decorators import dag, task
from airflow.hooks.base import BaseHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pendulum
from datetime import datetime, timedelta
from typing import List, Dict
import random
import json
import boto3

@dag(
    dag_id="dag_minio_postgres_pipeline_v2",
    schedule_interval=None,
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    tags=["minio", "postgres", "boto3"],
)
def minio_postgres_pipeline():

    @task
    def generate_data() -> List[Dict]:
        start_date = datetime(2023, 1, 1)
        data = []
        for i in range(100):
            order_date = start_date + timedelta(days=random.randint(0, 364))
            data.append({
                "order_id": f"ORDER-{i + 1:04d}",
                "product_id": f"PROD-{random.randint(1, 20):03d}",
                "quantity": random.randint(1, 5),
                "price": round(random.uniform(10.0, 200.0), 2),
                "order_date": order_date.strftime("%Y-%m-%d"),
            })
        return data

    @task
    def upload_to_minio(sales_data: List[Dict]) -> str:
        conn = BaseHook.get_connection("minio_default")
        s3 = boto3.client(
            "s3",
            aws_access_key_id=conn.login,
            aws_secret_access_key=conn.password,
            endpoint_url=conn.host
        )

        # Generate unique filename
        now = pendulum.now("Asia/Bangkok").format("YYYYMMDDHHmmss")
        key = f"sales_data_{now}.json"

        s3.put_object(
            Bucket="my-bucket",
            Key=key,
            Body=json.dumps(sales_data),
            ContentType="application/json"
        )

        print(f"Uploaded file: {key}")
        return key

    @task
    def download_from_minio(key: str) -> List[Dict]:
        conn = BaseHook.get_connection("minio_default")
        s3 = boto3.client(
            "s3",
            aws_access_key_id=conn.login,
            aws_secret_access_key=conn.password,
            endpoint_url=conn.host
        )

        response = s3.get_object(Bucket="my-bucket", Key=key)
        content = response['Body'].read().decode("utf-8")
        print(f"Downloaded file: {key}")
        return json.loads(content)

    @task
    def load_to_postgres(sales_data: List[Dict]):
        pg_hook = PostgresHook(postgres_conn_id="postgres_default")

        create_table_sql = """
        CREATE TABLE IF NOT EXISTS sales_data (
            order_id TEXT,
            product_id TEXT,
            quantity INT,
            price FLOAT,
            order_date DATE
        );
        """

        pg_hook.run(create_table_sql)

        rows = [
            (row['order_id'], row['product_id'], row['quantity'], row['price'], row['order_date'])
            for row in sales_data
        ]
        pg_hook.insert_rows(table="sales_data", rows=rows)

    @task
    def log_and_report():
        pg_hook = PostgresHook(postgres_conn_id="postgres_default")
        pg_hook.run("""
            CREATE TABLE IF NOT EXISTS etl_tracking (
                run_time TIMESTAMP,
                status TEXT
            );
        """)
        pg_hook.run("""
            INSERT INTO etl_tracking (run_time, status)
            VALUES (NOW(), 'SUCCESS');
        """)

        count = pg_hook.get_first("SELECT COUNT(*) FROM sales_data;")[0]
        print(f"Total rows in sales_data table: {count}")

    # DAG Task Flow
    data = generate_data()
    file_key = upload_to_minio(data)
    downloaded = download_from_minio(file_key)
    loaded = load_to_postgres(downloaded)
    log = log_and_report()

    loaded >> log

dag = minio_postgres_pipeline()
