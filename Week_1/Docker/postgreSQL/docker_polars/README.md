# Converting our data ingestion to use Polars

## Starting with the results
Polars Total Time Taken: 6.958 seconds
Pandas Total Time Taken: 46.041 seconds

Polars is roughly 85% faster than Pandas for our very simple ingestion script. 

## What is Polars
Polars is a data frame library, similar to Pandas. It is built in Rust and optimised for speed. This isn't an 'Intro to Polars' article OR a 'Pandas v Polars' article (of which there are many online - including some by a course Tutor [Luis](https://medium.com/gitconnected/polars-vs-dask-fighting-on-parallel-computing-f2a17a100274)). So I'll leave the intro at that.

## Reading CSV data with Polars
Polars provides similar functionality to Pandas for loading from CSV. The main function read_csv loads all data from a file (options for n rows of course) into a dataframe which can be manipulated. 

In our case, we want to batch load from the csv and pass each batch to the database. For that we can use read_csv_batched  function
```python
    csv_reader = pl.read_csv_batched(file_name, dtypes=schema.dtypes)
```
This returns a BatchedCsvReader type, which we can call next_batches on to load an array of dataframes corresponding to each batch.
```python
while (batches := csv_reader.next_batches(1)) is not None:
    print(batches[0].head(1))
```
Here we are looping through our csv_reader, loading each batch and printing the first row from it. Notice the walrus operator we are using to set batches
```python
batches := csv_reader.next_batches(1)
```
That allows to set batches within the while statement. If csv_reader is exhausted, it will return None, exiting the While loop.

## Writing to the database
The write_database function allows us to write the dataframe back to the DB. We can use 1 of 2 engines to accomplish this - the default, sqlalchemy (which we also used for Pandas library) or ADBC. In the SQLAlchemy approach, Polars actually converts the df to a Pandas df backed by PyArrow and then uses SQLAlchemy methods on the Pandas df. ADBC or Arrow Database Connectivity is an engine supported by the Apache Arrow project. ADBC is in its infancy still and many databases are still not [feature complete](https://arrow.apache.org/adbc/main/driver/status.html). For want we are looking to accomplish, ADBC will work. Note on the link though that PostgreSQl does not have full type support. This is something I noticed myself when testing, as the full set of Polars DTypes aren't supported by adbc_driver_postgresql. 

To use ADBC with Polars, we need to install additional packages. Back in our Dockerfile, we should have
```Dockerfile
FROM python:3.12.1

RUN pip install polars adbc_driver_manager adbc-driver-postgresql pyarrow

WORKDIR /app
COPY ingest_data_polars.py ingest_data_polars.py

ENTRYPOINT [ "python", "ingest_data_polars.py" ]
```

## Adding Schema Data through Attached Volume
To speed things up further, I wanted to pass polars the data types of each column. Polars, by default, will use the first 100 rows of data to infer the data type of each column. If the first 100 rows are null or it is ambiguous, the dtype defaults to string.

We could add a dictionary for each table within the main ingest_data_polars.py script, however, each time we wanted to change the data type, we would need to rebuild our image. Ideally we would avoid that since this is really meta data/configuration data and not application code. 

To avoid this, we can pass a volume across when running the image. Within this folder, we can have add a config file for each table. Any time we want to update the meta data within it, we can update the file directly. The next time the image is run, it will have access to the latest version of these files. 

```bash
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

