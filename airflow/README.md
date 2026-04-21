# Bicycle Data Pipeline (London Santander Cycles)

This is a Data Engineering project that extracts bicycle usage data from the London TFL API, processes it into Parquet format, and loads it into Google Cloud (GCS & BigQuery).

## Technical Stack
- **Orchestration:** Apache Airflow 3.2.0
- **Environment Management:** uv
- **Cloud Provider:** Google Cloud Platform (GCS, BigQuery)
- **Infrastructure:** Terraform

## Project Structure
```text
.
├── airflow/
│   ├── dags/          # DAG definitions (bike_pipeline_dag.py)
│   ├── scripts/       # Logic for Extract and Load (extract.py, load_bq.py)
│   └── airflow.db     # Local metadata database
├── terraform/         # Infrastructure as Code and Service Account keys
└── pyproject.toml     # Python dependencies managed by uv

Setup and Initialization
1. Environment Variables
Airflow and Google Cloud require specific environment variables to be set in your shell:

Bash
export AIRFLOW_HOME=$(pwd)/airflow
export PYTHONPATH=$PYTHONPATH:$(pwd)/airflow
export GOOGLE_APPLICATION_CREDENTIALS=$(pwd)/terraform/keyproject.json
export AIRFLOW__CORE__LOAD_EXAMPLES=False
2. Initialize the Database
If running for the first time or after a reset:

Bash
uv run airflow db migrate
Running the Pipeline
Option 1: Testing Atomic Tasks (Recommended for Dev)
To test the extraction task without running the full scheduler:

Bash
uv run airflow tasks test bike_pipeline extract_upload_gcs 2026-04-17
Option 2: Running the Full Airflow UI
To start the Airflow 3.2 engine and view the dashboard:

Bash
# Start the Scheduler (Brain)
uv run airflow scheduler

# Start the API Server (UI) - In a separate terminal
uv run airflow api-server
Accessing the UI
Open the Ports tab in your environment.

Locate port 8080 and open it in your browser.

Login: Default username is admin. The password can be found in airflow/standalone_admin_password.txt.

Data Pipeline Logic
Extract: Downloads CSV data from TFL, converts it to Parquet for performance.

Stage: Uploads Parquet files to a GCS bucket.

Load: Transfers data from GCS into BigQuery tables.

1. Environment Initialization
Before running Airflow, I configured the shell to remember the Google Cloud credentials and project paths.

Bash
# Add exports to .bashrc for persistence across terminal sessions
echo 'export GOOGLE_APPLICATION_CREDENTIALS=/workspaces/bicycle_project/bicycle-pipeline/terraform/keyproject.json' >> ~/.bashrc
echo 'export AIRFLOW_HOME=/workspaces/bicycle_project/bicycle-pipeline/airflow' >> ~/.bashrc
echo 'export PYTHONPATH=$PYTHONPATH:/workspaces/bicycle_project/bicycle-pipeline/airflow' >> ~/.bashrc

# Refresh the shell
source ~/.bashrc
2. Database & Connection Setup
After initializing the Airflow database, I manually injected the Google Cloud connection into the internal Metadata DB.

Bash
# Reset and migrate the database to ensure a clean state
uv run airflow db reset -y
uv run airflow db migrate

# Add the GCP connection (The Airflow "Passport")
uv run airflow connections add 'google_cloud_default' \
    --conn-type 'google_cloud_platform' \
    --conn-extra '{"project": "stately-math-492314-u2", "key_path": "/workspaces/bicycle_project/bicycle-pipeline/terraform/keyproject.json"}'
3. Task Execution & Testing
I used the Airflow CLI to test individual tasks in the dependency chain to verify the logic before doing a full DAG run.

Bash
# Force Airflow to scan for DAG changes
uv run airflow dags reserialize

# Verify the DAG is found and error-free
uv run airflow dags list
uv run airflow dags list-import-errors

# Run Step 2: Load raw data to BigQuery
uv run airflow tasks test bike_pipeline load_temp_table 2026-04-19

# Run Step 3: Transform into Partitioned/Clustered table
uv run airflow tasks test bike_pipeline create_partitioned_clustered_table 2026-04-19
4. BigQuery Maintenance (Troubleshooting)
Because partitioning specs cannot be changed on an existing table, I used this Python one-liner to "nuke" the old table when schema updates were required.

Bash
# Delete table to allow a new partitioning spec to be applied
uv run python3 -c "from google.cloud import bigquery; client = bigquery.Client(); client.delete_table('stately-math-492314-u2.bicycle_dataset.stg_santander', not_found_ok=True); print('Table Deleted')"
💡 Why include these?