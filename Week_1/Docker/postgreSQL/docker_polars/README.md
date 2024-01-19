# Converting our data ingestion to use Polars

## Starting with the results
Polars Total Time Taken: 6.958 seconds
Pandas Total Time Taken: 46.041 seconds

Polars is roughly 85% faster than Pandas for our very simple ingestion script. 

## What is Polars
Polars is a data frame library, similar to Pandas. It is built in Rust and optimised for speed. This isn't an 'Intro to Polars' article OR a 'Pandas v Polars' article (of which there are many online - including some by a course Tutor [Luis](https://medium.com/gitconnected/polars-vs-dask-fighting-on-parallel-computing-f2a17a100274)). So I'll leave the intro at that.

## Reading CSV data with Polars
Polars provides similar functionality to Pandas for loading from CSV. The main function read_csv loads all data from a file (options for n rows of course) into a dataframe which can be manipulated. 

In our case, we want to batch load from the csv and pass each batch to the database. For that we can use read_csv_batched
```python
    csv_reader = pl.read_csv_batched(file_name, dtypes=schema.dtypes)
```


## Adding Schema Data through Attached Volume
To speed things up further, I wanted to pass polars the data types of each column. Polars, by default, will use the first 100 rows of data to infer the data type of each column. If the first 100 rows are null or it is ambiguous, the dtype defaults to string.

We could add a dictionary for each table within the main ingest_data_polars.py script, however, each time we wanted to change the data type, we would need to rebuild our image. Ideally we would avoid that since this is really meta data/configuration data and not application code. 

To avoid this, we can pass a volume across when running the image. Within this folder, we can have add a config file for each table. Any time we want to update the meta data within it, we can update the file directly. The next time the image is run, it will have access to the latest version of these files. 

```Shell
docker run \
    --network=postgresql_default \
    -v D:/Development/data-engineering-zoomcamp-2024/Week_1/Docker/postgreSQL/docker_polars/config:/app/config \
    taxi_ingest_pl:v001 \
    --user=root \
    --password=$PGADMIN_DEFAULT_PASSWORD \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table_name=zone_data \
    --url=${ZONE_DATA}     
```

Above, you can see we have mapped our local config folder to the /app/config folder.

