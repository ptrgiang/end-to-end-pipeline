from airflow.decorators import dag, task
from typing import List, Dict  # ✅ FIXED
import pendulum
from datetime import datetime, timedelta
import random

@dag(
    dag_id="test_minio_connection",
    schedule_interval=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["minio", "boto3"],
)
def decorated_pipeline():
    @task
    def generate_data() -> List[Dict]:  # ✅ FIXED
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
    def upload_to_minio(sales_data: List[Dict]):  # ✅ FIXED
        import boto3
        import json

        s3 = boto3.client(
            "s3",
            aws_access_key_id="minioadmin",
            aws_secret_access_key="minioadmin",
            endpoint_url="http://minio:9000"
        )

        # Make sure bucket exists
        bucket_name = "my-bucket"
        if bucket_name not in [b['Name'] for b in s3.list_buckets().get('Buckets', [])]:
            s3.create_bucket(Bucket=bucket_name)

        s3.put_object(
            Bucket=bucket_name,
            Key="sales_data.json",
            Body=json.dumps(sales_data),
            ContentType="application/json"
        )

    sales = generate_data()
    upload_to_minio(sales)

dag = decorated_pipeline()
