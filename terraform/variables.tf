variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "Default GCP region"
  type        = string
}

variable "bucket_name" {
  description = "Name of the GCS bucket"
  type        = string
}

variable "dataset_id" {
  description = "BigQuery dataset ID"
  type        = string
}

variable "bq_location" {
  description = "BigQuery dataset location"
  type        = string
}
variable "lifecycle_age" {
  description = "Days before objects are deleted"
  type        = number
}