Welcome to your new dbt project!

### Using the starter project

Try running the following commands:
- dbt run
- dbt test


Step 5: Data Transformation with dbt
In this phase, I implemented dbt (Data Build Tool) to manage the transformation layer of the ELT pipeline. This ensures that business logic is version-controlled, modular, and optimized for analytics.

📂 The Multi-Layered Modeling Approach
I followed the industry-standard "Medallion" architecture to process the data:

Source Layer: Defined the connection to the partitioned BigQuery table (stg_santander).

Staging Layer (stg_trip_data):

Abstraction: Created a view to act as a buffer between raw data and final models.

Cleanup: Standardized legacy column names from the raw source into clean snake_case (e.g., StartStation Id → start_station_id).

Marts Layer (Fact & Dimension Tables):

facts_trips: The core transactional table containing rental IDs, durations, and dates. I added calculated metrics such as duration_minutes.

dim_stations: A deduplicated lookup table containing all unique bike stations, enabling a efficient Star Schema design.

🚀 Key Features & Optimization
Dry-Run Validation: Used dbt run to compile SQL logic and validate against the BigQuery schema before materializing data.

Materialization Strategy:

Views were used for staging to save storage costs.

Tables were used for marts to provide high-performance query speeds for BI tools.

Lineage Tracking: Utilized the ref() function to build a Directed Acyclic Graph (DAG) of the models, ensuring stg_trip_data always builds before facts_trips.

💻 Commands Used for dbt
Bash
# 1. Initialize dbt and install dependencies
uv pip install dbt-bigquery
uv run dbt init dbt_transformation

# 2. Validate connection to BigQuery
uv run dbt debug

# 3. Build the models (Staging -> Marts)
uv run dbt run

# 4. (Optional) Generate and view lineage documentation
uv run dbt docs generate
uv run dbt docs serve --port 8080