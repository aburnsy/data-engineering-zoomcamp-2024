## Big Query

```

## Question 1: What is count of records for the 2022 Green Taxi Data??
- `840,402`
```SQL
CREATE OR REPLACE EXTERNAL TABLE `terraformproject-123489.green_taxi.external_green_taxi_2022`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://zoomcamp_week3_bigquery_andy_burns/green_taxi']
);
-- https://storage.cloud.google.com/zoomcamp_week3_bigquery_andy_burns/green_taxi

CREATE OR REPLACE TABLE `terraformproject-123489.green_taxi.green_taxi_2022` AS
SELECT * FROM `terraformproject-123489.green_taxi.external_green_taxi_2022`;

SELECT count(*) FROM `terraformproject-123489.green_taxi.green_taxi_2022`;
```

## Question 2. Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.
What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?
- `0 MB for the External Table and 6.41MB for the Materialized Table`
```SQL
SELECT count(distinct PULocationID) FROM `terraformproject-123489.green_taxi.green_taxi_2022`;
```

## Question 3. How many records have a fare_amount of 0?
- `1,622`
```SQL
SELECT count(*) FROM `terraformproject-123489.green_taxi.green_taxi_2022`
WHERE fare_amount = 0;
```

## Question 4. What is the best strategy to make an optimized table in Big Query if your query will always order the results by PUlocationID and filter based on lpep_pickup_datetime? (Create a new table with this strategy)
- `Partition by lpep_pickup_datetime Cluster on PUlocationID`
```SQL
SELECT distinct vendor_id 
FROM mage.green_taxi
```
> SQL Used for Question

## Question 5. Data Transformation
- `12.82 MB for non-partitioned table and 1.12 MB for the partitioned table`
```SQL
CREATE OR REPLACE TABLE terraformproject-123489.green_taxi.green_taxi_2022_pd
PARTITION BY DATE(lpep_pickup_datetime)
CLUSTER BY PUlocationID AS
SELECT * FROM terraformproject-123489.green_taxi.green_taxi_2022;

SELECT distinct PULocationID 
FROM terraformproject-123489.green_taxi.green_taxi_2022_pd
WHERE DATE(lpep_pickup_datetime) between DATE('2022-06-01') AND DATE('2022-06-30');

SELECT distinct PULocationID 
FROM terraformproject-123489.green_taxi.green_taxi_2022
WHERE DATE(lpep_pickup_datetime) between DATE('2022-06-01') AND DATE('2022-06-30')
```


## Question 6. Data Exporting
- `GCP Bucket`


## Question 7. It is best practice in Big Query to always cluster your data
- `True`


## Question 8. It is best practice in Big Query to always cluster your data
- `0`
> BQ stores meta data for each partition