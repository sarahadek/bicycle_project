import requests
import pandas as pd
from io import StringIO, BytesIO
from google.cloud import storage
import pyarrow as pa
import pyarrow.parquet as pq

# ----------------------------
# CONFIG
# ----------------------------
BUCKET_NAME = "bicycle-data-bucket"  # change if needed

URLS = [
    "https://cycling.data.tfl.gov.uk/usage-stats/01aJourneyDataExtract10Jan16-23Jan16.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/01bJourneyDataExtract24Jan16-06Feb16.csv",
    "https://cycling.data.tfl.gov.uk/usage-stats/02aJourneyDataExtract07Fe16-20Feb2016.csv",
]

# ----------------------------
# INIT GCS CLIENT
# ----------------------------
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

# ----------------------------
# MAIN EXTRACT FUNCTION
# ----------------------------
def extract_and_upload():
    headers = {"User-Agent": "Mozilla/5.0"}

    success = 0

    for i, url in enumerate(URLS, 1):
        print(f"\nProcessing {i}/{len(URLS)}: {url}")

        try:
            # 1. Download CSV
            response = requests.get(url, headers=headers, timeout=60)
            response.raise_for_status()

            # 2. Load into pandas
            df = pd.read_csv(StringIO(response.text))

            # 3. Convert to Parquet in memory
            table = pa.Table.from_pandas(df)
            buffer = BytesIO()
            pq.write_table(table, buffer)
            buffer.seek(0)

            # 4. Create GCS file path
            filename = url.split("/")[-1].replace(".csv", ".parquet")
            blob_path = f"raw/santander/{filename}"

            blob = bucket.blob(blob_path)

            # 5. Upload to GCS
            blob.upload_from_file(buffer, content_type="application/octet-stream")

            print(f"Uploaded to gs://{BUCKET_NAME}/{blob_path}")
            success += 1

        except Exception as e:
            print(f"FAILED: {url}")
            print(f"Reason: {e}")

    print("\nDONE")
    print(f"Successful uploads: {success}/{len(URLS)}")


# ----------------------------
# RUN
# ----------------------------
if __name__ == "__main__":
    extract_and_upload()
