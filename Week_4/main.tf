terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.13.0"
    }
  }
}

provider "google" {
  project     = "terraformproject-123489"
  region      = "us-central1"
  credentials = "D:/Development/data-engineering-zoomcamp-2024/config/terraformproject-123489-7ebacaa3e92b.json"

}

resource "google_storage_bucket" "zoomcamp_week4_bigquery_andy_burns" {
  name          = "zoomcamp_week4_bigquery_andy_burns"
  location      = "US"
  force_destroy = true # Delete the bucket even if data is present

  public_access_prevention = "enforced" # Don't allow public access


  # Delete files older than 1 day by default
  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "Delete"
    }
  }
}

resource "google_bigquery_dataset" "trips_data_all" {
  dataset_id                  = "trips_data_all"
  friendly_name               = "trips_data_all"
  description                 = "Taxi data for week 4"
  location                    = "US"
  default_table_expiration_ms = 360000000

  labels = {
    env = "default"
  }

}
