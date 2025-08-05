import json
from minio import Minio
import psycopg2

def main():
    # MinIO connection
    minio_client = Minio(
        "minio:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )

    # Download data from MinIO
    try:
        response = minio_client.get_object("my-bucket", "sales_data.json")
        sales_data = json.loads(response.read())
    finally:
        response.close()
        response.release_conn()

    # PostgreSQL connection
    conn = psycopg2.connect(
        host="postgres",
        database="airflow",
        user="airflow",
        password="airflow"
    )
    cur = conn.cursor()

    # Create table if not exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            order_id VARCHAR(255) PRIMARY KEY,
            product_id VARCHAR(255),
            quantity INTEGER,
            price NUMERIC,
            order_date DATE
        );
    """)

    # Insert data into PostgreSQL
    for record in sales_data:
        cur.execute("""
            INSERT INTO sales (order_id, product_id, quantity, price, order_date)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (order_id) DO NOTHING;
        """, (
            record["order_id"],
            record["product_id"],
            record["quantity"],
            record["price"],
            record["order_date"]
        ))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
