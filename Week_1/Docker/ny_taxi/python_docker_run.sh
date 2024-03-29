#!/bin/sh

TAXI_DATA="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"
ZONE_DATA="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"

# python ingest_data.py \
#     --user=root \
#     --password=$PGADMIN_DEFAULT_PASSWORD \
#     --host=localhost \
#     --port=5432 \
#     --db=ny_taxi \
#     --table_name=yellow_taxi_trips \
#     --url=${URL}

# TAXI USING PANDAS
# docker run \
#     --network=ny_taxi_default \
#     taxi_ingest:v001 \
#     --user=root \
#     --password=$PGADMIN_DEFAULT_PASSWORD \
#     --host=pgdatabase \
#     --port=5432 \
#     --db=ny_taxi \
#     --table_name=yellow_taxi_trips \
#     --url=${TAXI_DATA} 

# # ZONE USING PANDAS
# docker run \
#     --network=ny_taxi_default \
#     taxi_ingest:v001 \
#     --user=root \
#     --password=$PGADMIN_DEFAULT_PASSWORD \
#     --host=pgdatabase \
#     --port=5432 \
#     --db=ny_taxi \
#     --table_name=zone \
#     --url=${ZONE_DATA} 

## TAXI USING POLARS
docker run \
    --network=ny_taxi_default \
    -v D:/Development/data-engineering-zoomcamp-2024/Week_1/Docker/ny_taxi/ingestion_polars/config:/app/config \
    taxi_ingest_pl:v001 \
    --user=root \
    --password=$PGADMIN_DEFAULT_PASSWORD \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi \
    --url=${TAXI_DATA} 

## ZONE USING POLARS
docker run \
    --network=ny_taxi_default \
    -v D:/Development/data-engineering-zoomcamp-2024/Week_1/Docker/ny_taxi/ingestion_polars/config:/app/config \
    taxi_ingest_pl:v001 \
    --user=root \
    --password=$PGADMIN_DEFAULT_PASSWORD \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table_name=zone \
    --url=${ZONE_DATA}     