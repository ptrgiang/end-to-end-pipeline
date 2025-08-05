# End-to-End Data Pipeline with Airflow, MinIO, and PostgreSQL

This project demonstrates a complete data pipeline using Apache Airflow for orchestration, MinIO for object storage (as a data lake), and PostgreSQL as a data warehouse. The pipeline is containerized using Docker.

## Architecture

The data processing system is designed with the following stages:

| ID  | Stage                        | Description                                                                                                                                                 | Tools                                  |
| --- | ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| 1.0 | Data Collection              | - Automatically call an API (e.g., Amazon) to retrieve data (sales, products, inventory, etc.) on a schedule. <br> - Save the raw files to MinIO.             | - API (e.g., Amazon) <br> - Airflow <br> - MinIO |
| 2.0 | Data Storage                 | - Set up MinIO as a Data Lake to store raw data. <br> - Use PostgreSQL as a Data Warehouse for structured data, ready for analysis.                           | - MinIO <br> - PostgreSQL              |
| 3.0 | ETL (Extract, Transform, Load) | - Build Python scripts to read raw data from MinIO, perform cleaning and transformation. <br> - Load the cleaned data into tables in PostgreSQL.             | - Airflow <br> - Python                |
| 4.0 | Orchestration & Monitoring   | - Use Airflow to orchestrate the entire pipeline (API -> MinIO -> PostgreSQL). <br> - Monitor the status and send alerts on failure.                         | - Airflow                              |
| 5.0 | CI/CD                        | - Store all code (DAGs, scripts) on a Git repository. <br> - Use a CI/CD tool (e.g., Jenkins, GitHub Actions) to automatically test and deploy new code.      | - Git <br> - Jenkins/GitHub Actions    |
| 6.0 | Data Access & Analysis       | - Connect BI tools to PostgreSQL for end-users to create reports. <br> - Dashboards with automatically refreshed data.                                        | - PostgreSQL <br> - Power BI/Tableau   |

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Create an environment file:**
    Create a `.env` file in the root of the project and add the following environment variables. You can change the values as you see fit.

    ```env
    # PostgreSQL
    POSTGRES_USER=airflow
    POSTGRES_PASSWORD=airflow
    POSTGRES_DB=airflow

    # MinIO
    MINIO_ROOT_USER=minioadmin
    MINIO_ROOT_PASSWORD=minioadmin

    # Airflow
    AIRFLOW_SECRET_KEY=your-super-secret-key
    ```

3.  **Build and run the containers:**
    ```bash
    docker-compose up --build
    ```

4.  **Access the services:**
    - **Airflow UI:** [http://localhost:8080](http://localhost:8080) (Login with `admin`/`admin`)
    - **MinIO UI:** [http://localhost:9001](http://localhost:9001) (Login with the `MINIO_ROOT_USER` and `MINIO_ROOT_PASSWORD` you set in the `.env` file)

## Project Structure

- `airflow/`: Contains Airflow configurations, DAGs, and plugins.
  - `dags/`: Airflow DAGs defining the pipelines.
  - `Dockerfile`: Dockerfile for the Airflow services.
  - `requirements.txt`: Python dependencies for Airflow.
- `docker-compose.yaml`: Defines the services, networks, and volumes for the project.
- `.env`: Environment variables for the services (not version controlled).
- `README.md`: This file.
