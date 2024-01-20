## Docker & SQL

## Question 1. Knowing docker tags
- `--rm`


## Question 2. Understanding docker first run 
- 0.42.0


## Question 3. Count records 
- 15612
```SQL
SELECT count(1)
FROM yellow_taxi
WHERE start_date = '2019-09-18'
AND end_date = '2019-09-18';
```
> SQL Used. Note: The ingestion scripts were amended to use Polars + transform the data. You can find those scripts [here](../Docker/ny_taxi/ingestion_polars/README.md)


## Question 4. Largest trip for each day
- 2019-09-26
```SQL
SELECT start_date
FROM yellow_taxi
WHERE trip_distance = (SELECT max(trip_distance) FROM yellow_taxi)
```

## Question 5. Three biggest pick up Boroughs
- "Brooklyn" "Manhattan" "Queens"
```SQL
SELECT z.borough
FROM yellow_taxi y
JOIN zone z ON y.start_location_id = z.location_id
WHERE y.start_date = '2019-09-18'
AND z.borough <> 'Unknown'
GROUP BY z.borough
HAVING sum(y.total_amount) > 50000
ORDER BY sum(y.total_amount) DESC
```


## Question 6. Largest tip
- JFK Airport
```SQL
SELECT en.zone
FROM yellow_taxi y
JOIN zone st ON y.start_location_id = st.location_id
JOIN zone en ON y.end_location_id = en.location_id
WHERE EXTRACT(MONTH FROM y.start_date) = 9
AND EXTRACT(YEAR FROM y.start_date) = 2019
AND st.zone = 'Astoria'
GROUP BY en.zone
ORDER BY max(y.tip_amount) DESC
LIMIT 1
```



## Terraform
## Question 7. Creating Resources
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.demo_dataset will be created
  + resource "google_bigquery_dataset" "demo_dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "andy-homework-dataset-name"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = false
      + effective_labels           = (known after apply)
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "US"
      + max_time_travel_hours      = (known after apply)
      + project                    = "terraformproject-123489"
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
      + terraform_labels           = (known after apply)
    }

  # google_storage_bucket.demo-bucket will be created
  + resource "google_storage_bucket" "demo-bucket" {
      + effective_labels            = (known after apply)
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "US"
      + name                        = "andy-homework-terra-bucket"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = (known after apply)
      + uniform_bucket_level_access = (known after apply)
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "AbortIncompleteMultipartUpload"
            }
          + condition {
              + age                   = 1
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: