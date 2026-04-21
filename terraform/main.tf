terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.27.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  # Configuration options
}

resource "google_storage_bucket" "bicycle_bucket" {
  name     = var.bucket_name
  location = var.region

  force_destroy = false

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = var.lifecycle_age
    }
  }
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.dataset_id
  location   = var.bq_location
}

