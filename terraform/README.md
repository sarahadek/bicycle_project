# 🚲 Bicycle Pipeline — Terraform Infrastructure

This Terraform project provisions the Google Cloud infrastructure required for the Bicycle Data Pipeline.

## 📦 Resources Created

* **Google Cloud Storage Bucket** — stores raw bicycle data
* **BigQuery Dataset** — stores staging and analytics tables
* **IAM Permissions** — enables secure access for pipeline components

---

## ⚙️ Prerequisites

* Google Cloud project with billing enabled
* Terraform installed
* Authenticated with GCP:

```bash
gcloud auth application-default login
```

---

## 🚀 Deployment

Initialize Terraform:

```bash
terraform init
```

Preview changes:

```bash
terraform plan
```

Apply infrastructure:

```bash
terraform apply
```

---

## 🧹 Cleanup

Destroy all resources:

```bash
terraform destroy
```

⚠️ This permanently deletes all provisioned infrastructure.

---

## 🌍 Configuration

Project ID and region are defined in `variables.tf`.

---

Infrastructure is fully reproducible and managed as code using Terraform.
