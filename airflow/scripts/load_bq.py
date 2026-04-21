from google.cloud import bigquery

PROJECT_ID = "stately-math-492314-u2"
DATASET_ID = "bicycle_dataset"
TABLE_ID = "stg_santander"

GCS_URI = "gs://bicycle-data-bucket/raw/santander/*.parquet"

def load_to_bigquery():
    client = bigquery.Client(project=PROJECT_ID)

    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition="WRITE_TRUNCATE",  # overwrite each run
    )

    job = client.load_table_from_uri(
        GCS_URI,
        table_ref,
        job_config=job_config
    )

    job.result()  # wait for completion

    print(f"Loaded data into {table_ref}")


if __name__ == "__main__":
    load_to_bigquery()
