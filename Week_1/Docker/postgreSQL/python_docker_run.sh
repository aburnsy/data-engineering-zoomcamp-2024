URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-01.csv.gz"
URL2="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"

# python ingest_data.py \
#     --user=root \
#     --password=$PGADMIN_DEFAULT_PASSWORD \
#     --host=localhost \
#     --port=5432 \
#     --db=ny_taxi \
#     --table_name=yellow_taxi_trips \
#     --url=${URL}

# docker run \
#     --network=pg-network \
#     --name ingestion \
#     taxi_ingest:v001 \
#     --user=root \
#     --password=$PGADMIN_DEFAULT_PASSWORD \
#     --host=pg-database \
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
    --table_name=zone \
    --url=${URL2} 
