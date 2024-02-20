#!/bin/sh

# docker build -t taxi_ingestion:v001 .

## TAXI USING POLARS
# docker run \
#     --network=ny_taxi_default \
#     -v D:/Development/data-engineering-zoomcamp-2024/Week_4/schema:/app/schema \
#     -v D:/Development/data-engineering-zoomcamp-2024/Week_4/config:/app/config \
#     taxi_ingestion:v001 \
#     --dataset_name=fhv \

# docker run \
#     --network=ny_taxi_default \
#     -v D:/Development/data-engineering-zoomcamp-2024/Week_4/schema:/app/schema \
#     -v D:/Development/data-engineering-zoomcamp-2024/Week_4/config:/app/config \
#     taxi_ingestion:v001 \
#     --dataset_name=green \

docker run \
    -v D:/Development/data-engineering-zoomcamp-2024/Week_4/schema:/app/schema \
    -v D:/Development/data-engineering-zoomcamp-2024/Week_4/config:/app/config \
    taxi_ingestion:v001 \
    --dataset_name=yellow \
        # --network=ny_taxi_default \