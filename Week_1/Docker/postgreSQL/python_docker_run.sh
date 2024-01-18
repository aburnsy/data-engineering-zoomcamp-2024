URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"
URL2="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"

# python ingest_data.py \
#     --user=root \
#     --password=$PGADMIN_DEFAULT_PASSWORD \
#     --host=localhost \
#     --port=5432 \
#     --db=ny_taxi \
#     --table_name=yellow_taxi_trips \
#     --url=${URL}

docker run \
    --network=postgresql_default \
    taxi_ingest:v001 \
    --user=root \
    --password=$PGADMIN_DEFAULT_PASSWORD \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL} 

# docker run \
#     --network=postgresql_default \
#     taxi_ingest:v001 \
#     --user=root \
#     --password=$PGADMIN_DEFAULT_PASSWORD \
#     --host=pgdatabase \
#     --port=5432 \
#     --db=ny_taxi \
#     --table_name=zone \
#     --url=${URL2} 

docker run \
    --network=postgresql_default \
    taxi_ingest_pl:v001 \
    --user=root \
    --password=$PGADMIN_DEFAULT_PASSWORD \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_data \
    --url=${URL} 