from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from datetime import datetime
import subprocess

# -------------------------
# IMPORT YOUR SCRIPTS
# -------------------------
from scripts.extract import extract_and_upload


# -------------------------
# DBT FUNCTION
# -------------------------
# Change this:
def run_dbt():
    # Use the path to your dbt folder in your codespace
    subprocess.run(["dbt", "run"], cwd="/workspaces/bicycle_project/bicycle-pipeline/dbt_transformations", check=True)


# -------------------------
# CONSTANTS
# -------------------------
PROJECT_ID = "stately-math-492314-u2"
DATASET = "bicycle_dataset"
TEMP_TABLE = "temp_santander"
FINAL_TABLE = "stg_santander"


# -------------------------
# DAG DEFAULT ARGS
# -------------------------
default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 1
}


# -------------------------
# DAG
# -------------------------
with DAG(
    dag_id="bike_pipeline",
    default_args=default_args,
    schedule="@daily",
    catchup=False
) as dag:

    # STEP 1 — Extract + upload to GCS
    extract_task = PythonOperator(
        task_id="extract_upload_gcs",
        python_callable=extract_and_upload
    )

    # STEP 2 — Load GCS → Temporary BigQuery Table
    load_temp_table = GCSToBigQueryOperator(
        task_id="load_temp_table",
        bucket="bicycle-data-bucket",
        source_objects=["raw/santander/*.parquet"],
        destination_project_dataset_table=f"{PROJECT_ID}.{DATASET}.{TEMP_TABLE}",
        source_format="PARQUET",
        write_disposition="WRITE_TRUNCATE",
    )

    # STEP 3 — Create Partitioned + Clustered Table
    # Updated SQL for Step 3 in your DAG
    create_partitioned_table = BigQueryInsertJobOperator(
        task_id="create_partitioned_clustered_table",
        configuration={
            "query": {
                "query": f"""
                    CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET}.{FINAL_TABLE}`
                    PARTITION BY rental_date
                    CLUSTER BY `StartStation Id`
                    AS
                    SELECT 
                        *,
                        -- format '%d/%m/%Y %H:%M' matches '05/02/2016 08:37'
                        DATE(PARSE_DATETIME('%d/%m/%Y %H:%M', `Start Date`)) AS rental_date
                    FROM `{PROJECT_ID}.{DATASET}.{TEMP_TABLE}`
                """,
                "useLegacySql": False,
            }
        }
    )

    # STEP 4 — Run dbt
    dbt_task = PythonOperator(
        task_id="run_dbt",
        python_callable=run_dbt
    )

    # -------------------------
    # DEPENDENCIES
    # -------------------------
    extract_task >> load_temp_table >> create_partitioned_table >> dbt_task
