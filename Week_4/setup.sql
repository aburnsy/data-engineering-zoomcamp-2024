CREATE OR REPLACE TABLE terraformproject-123489.trips_data_all.yellow_tripdata as
SELECT * FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2020`
UNION ALL
SELECT * FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2019`;

CREATE OR REPLACE TABLE terraformproject-123489.trips_data_all.green_tripdata as
SELECT * FROM `bigquery-public-data.new_york_taxi_trips.tlc_green_trips_2020`
UNION ALL
SELECT * FROM `bigquery-public-data.new_york_taxi_trips.tlc_green_trips_2019`;

-- CREATE OR REPLACE TABLE terraformproject-123489.trips_data_all.fhv_tripdata as
-- SELECT * FROM `bigquery-public-data.new_york_taxi_trips.tlc_green_trips_2020`
-- UNION ALL
-- SELECT * FROM `bigquery-public-data.new_york_taxi_trips.tlc_fhv_2019`;

ALTER TABLE `terraformproject-123489.trips_data_all.yellow_tripdata`
  RENAME COLUMN vendor_id TO VendorID;
ALTER TABLE `terraformproject-123489.trips_data_all.yellow_tripdata`
  RENAME COLUMN pickup_datetime TO tpep_pickup_datetime;
ALTER TABLE `terraformproject-123489.trips_data_all.yellow_tripdata`
  RENAME COLUMN dropoff_datetime TO tpep_dropoff_datetime;
ALTER TABLE `terraformproject-123489.trips_data_all.yellow_tripdata`
  RENAME COLUMN rate_code TO RatecodeID;
ALTER TABLE `terraformproject-123489.trips_data_all.yellow_tripdata`
  RENAME COLUMN imp_surcharge TO improvement_surcharge;
ALTER TABLE `terraformproject-123489.trips_data_all.yellow_tripdata`
  RENAME COLUMN pickup_location_id TO PULocationID;
ALTER TABLE `terraformproject-123489.trips_data_all.yellow_tripdata`
  RENAME COLUMN dropoff_location_id TO DOLocationID;

  -- Fixes green table schema
ALTER TABLE `terraformproject-123489.trips_data_all.green_tripdata`
  RENAME COLUMN vendor_id TO VendorID;
ALTER TABLE `terraformproject-123489.trips_data_all.green_tripdata`
  RENAME COLUMN pickup_datetime TO lpep_pickup_datetime;
ALTER TABLE `terraformproject-123489.trips_data_all.green_tripdata`
  RENAME COLUMN dropoff_datetime TO lpep_dropoff_datetime;
ALTER TABLE `terraformproject-123489.trips_data_all.green_tripdata`
  RENAME COLUMN rate_code TO RatecodeID;
ALTER TABLE `terraformproject-123489.trips_data_all.green_tripdata`
  RENAME COLUMN imp_surcharge TO improvement_surcharge;
ALTER TABLE `terraformproject-123489.trips_data_all.green_tripdata`
  RENAME COLUMN pickup_location_id TO PULocationID;
ALTER TABLE `terraformproject-123489.trips_data_all.green_tripdata`
  RENAME COLUMN dropoff_location_id TO DOLocationID;