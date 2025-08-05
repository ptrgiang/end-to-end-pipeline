import json
import random
from datetime import datetime, timedelta

def generate_sales_data():
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    data = []
    for i in range(100):
        order_date = start_date + timedelta(days=random.randint(0, 364))
        data.append({
            "order_id": f"ORDER-{i+1:04d}",
            "product_id": f"PROD-{random.randint(1, 20):03d}",
            "quantity": random.randint(1, 5),
            "price": round(random.uniform(10.0, 200.0), 2),
            "order_date": order_date.strftime("%Y-%m-%d"),
        })
    return data

if __name__ == "__main__":
    sales_data = generate_sales_data()
    with open("/tmp/sales_data.json", "w") as f:
        json.dump(sales_data, f, indent=4)
