🚲 London Santander Cycles: End-to-End ELT Pipeline
This project demonstrates a production-grade ELT (Extract, Load, Transform) pipeline. It automates the ingestion of London Santander Cycle (TFL) data into Google Cloud, optimizes it for high-performance analytics using dbt, and visualizes key urban mobility insights in Power BI.
🚀 Getting Started
1. Build the Image
We use a Multi-stage build powered by uv to keep the image lightweight and fast.

Bash
docker build -t bicycle-pipeline:v1 .
2. Run with Docker Compose
The easiest way to start the container with all necessary environment variables and volume mounts:

Bash
docker-compose up
🛠️ Technical Stack
Infrastructure: Terraform (Infrastructure as Code)

Orchestration: Apache Airflow 3.2.0 (running with uv)

Storage: Google Cloud Storage (Data Lake)

Warehouse: Google BigQuery (Partitioned & Clustered)

Transformation: dbt (Data Build Tool)

Visualization: Power BI

🏗️ 1. Infrastructure as Code (Terraform)
The environment is fully reproducible, managed via Terraform to provision GCP resources securely.

Resources: GCS Buckets (Raw Landing), BigQuery Datasets, and IAM Service Accounts.

Key Command: terraform apply

🌪️ 2. Orchestration (Airflow)
Airflow manages the lifecycle of the data. The pipeline is designed to be idempotent and handles nearly 1 million rows of trip data per run.

Pipeline Logic:
Extract: Python scripts pull CSV data from the TFL API and convert it to Parquet for storage efficiency.

Stage: Uploads Parquet files to GCS.

Load: Ingests data into BigQuery temporary tables.

Optimize: A dedicated task handles the creation of a Partitioned (by Date) and Clustered (by Station) table to minimize query costs.

Bash
# Start the engine
uv run airflow scheduler
uv run airflow api-server
💎 3. Data Transformation (dbt)
Using the Medallion Architecture, raw data is shaped into analytical "Gold" tables.

Staging Layer (stg_trip_data): A view that standardizes legacy column names (e.g., StartStation Id → start_station_id) and casts data types.

Marts Layer (facts_trips & dim_stations):

Built a Star Schema to improve join performance.

Calculated new metrics like duration_minutes from raw seconds.

Command: uv run dbt run

📊 4. Business Intelligence & Insights
The final consumption layer consists of three targeted Power BI Dashboards connected via DirectQuery to BigQuery.

📈 Key Business Insights Derived:
Dashboard 1: Operational Demand
Peak Usage Hours: Identified rush-hour surges to assist in bike redistribution planning for jan 10 to feb 24 2016.

Station Heatmap: Visualized high-churn locations to identify docking station bottlenecks.

Dashboard 2: Maintenance & Safety
Fleet Stress Test: Isolated specific bike_ids with the highest cumulative usage duration (thousands of minutes) to trigger preventative maintenance.

Active Fleet Count: Real-time tracking of unique bikes in circulation.

Dashboard 3: Urban Planning & Growth
Trip Distribution: Analyzed "Last Mile" vs. "Leisure" behavior. A spike in <10 min trips indicates a heavy reliance on the network for commuting.

Station Imbalance: Spotted "Dead End" stations where bikes accumulate but rarely depart, helping optimize truck redistribution routes.

🚀 Getting Started
Prerequisites
GCP Project ID: stately-math-492314-u2

Service Account Key: Located at terraform/keyproject.json

Python Environment: Managed via uv

Installation & Run
Infra: cd terraform && terraform apply

Airflow: uv run airflow dags reserialize

Transform: cd dbt_transformation && uv run dbt run

Visualize: Open analytics/London_Bikes_Dashboard.pbip in Power BI Desktop.

🎓 Learning Summary
This project showcases the transition from a "Scripting" mindset to a "Systems" mindset. By implementing partitioning, dbt modeling layers, and a Star Schema, the pipeline is not only functional but cost-effective and scalable for large-scale urban data analysis.