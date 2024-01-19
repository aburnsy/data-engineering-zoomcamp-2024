# Converting our data ingestion to use Polars + Some general improvements to the script

## What is Polars
Polars is a data frame library, similar to Pandas. It is built in Rust and optimised for speed. This isn't an 'Intro to Polars' article OR a 'Pandas v Polars' article (of which there are many online - including some by a course Tutor [Luis](https://medium.com/gitconnected/polars-vs-dask-fighting-on-parallel-computing-f2a17a100274)). So I'll leave the intro at that.

## Starting with the results
Polars Total Time Taken: 6.958 seconds

Pandas Total Time Taken: 46.041 seconds

Polars is roughly 85% faster than Pandas for our very simple ingestion script. 

**Note** that this isn't a perfect comparison. In my Polars script, I am creating a handful of new fields. In Polars too I am passing the dtypes of the fields, which does have an impact.


## Updating Our Codebase


### Reading CSV data with Polars
Polars provides similar functionality to Pandas for loading from CSV. The main function read_csv loads all data from a file (options for n rows of course) into a dataframe which can be manipulated. 

In our case, we want to batch load from the csv and pass each batch to the database. For that we can use read_csv_batched  function
```python
    csv_reader = pl.read_csv_batched(file_name)
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
That allows to set batches within the while statement. If csv_reader is exhausted, it will return None, exiting the While loop. The 1 here refers to the number of chunks we want to fetch at any one time. We could fetch multiple chunks and concatenate them before passing to the database, but the DB will be the bottleneck in our case, so its best to leave that set to 1 for now.

### Writing to the database
The write_database function allows us to write the dataframe back to the DB. We can use 1 of 2 engines to accomplish this - the default, sqlalchemy (which we also used for Pandas library) or ADBC. In the SQLAlchemy approach, Polars actually converts the df to a Pandas df backed by PyArrow and then uses SQLAlchemy methods on the Pandas df. ADBC or Arrow Database Connectivity is an engine supported by the Apache Arrow project. ADBC is in its infancy still and many databases are still not [feature complete](https://arrow.apache.org/adbc/main/driver/status.html). For want we are looking to accomplish, ADBC will work. Note on the link though that PostgreSQl does not have full type support. This is something I noticed myself when testing, as the full set of Polars DTypes aren't supported by adbc_driver_postgresql. 

To use ADBC with Polars, we need to install additional packages. Back in our Dockerfile, we should have
```Dockerfile
FROM python:3.12.1

RUN pip install polars adbc_driver_manager adbc-driver-postgresql pyarrow

WORKDIR /app
COPY ingest_data_polars.py ingest_data_polars.py

ENTRYPOINT [ "python", "ingest_data_polars.py" ]
```

Back in our Python script, we can now export directly to the database
```python
# Setup connection to PG
connection = f"postgresql://{user}:{password}@{host}:{port}/{db}"

# Batch the csv file for reading later
csv_reader = pl.read_csv_batched(file_name)

# First chunk should replace existing table
if_table_exists = "replace"

# Loop through all csv data
while (batches := csv_reader.next_batches(1)) is not None:
    time_start = time()
    record_counts = (
        batches[0]
        .write_database(
            table_name=table_name,
            connection=connection,
            engine="adbc",
            if_table_exists=if_table_exists,
        )
    )

    # After the first chunk, we need to append records
    if_table_exists = "append"
```
Notice that we are amending the if_table_exists variable after the first run. Otherwise we would constantly be replacing the table with the latest chunk from the csv file. 

### Passing dtypes
To speed things up further, we can pass Polars the data types of our fields in the csv file. Polars, by default, will use the first 100 rows of data to infer the data type of each column. If the first 100 rows are null or it is ambiguous, the dtype defaults to string. We want to prevent this. If we have lots of columns or if we ask Polars to check more than 100 rows (through the infer_schema_length parameter), this could also impact our ingestion performance. Finally, Polars tends to prefer larger memory data types than smaller (though I can't find this exactly in their documenation). It seems to default to Int64 for rows which might only contain 1 and 2. 

To pass the dtypes, we use the dtypes parameter in the read_csv and read_csv_batched functions. dtypes should be an OrderedDict Type. For the yellow taxi data, it might look like this
```python
# Batch the csv file for reading later
from collections import OrderedDict
dtypes = OrderedDict(
    {
        "VendorID": pl.Int32,
        "lpep_pickup_datetime": pl.Datetime(time_unit="us", time_zone=None),
        "lpep_dropoff_datetime": pl.Datetime(time_unit="us", time_zone=None),
        "store_and_fwd_flag": pl.Categorical,
        "RatecodeID": pl.Int32,
        "PULocationID": pl.Int32,
        "DOLocationID": pl.Int32,
        "passenger_count": pl.Int32,
        "trip_distance": pl.Float32,
        "fare_amount": pl.Float32,
        "extra": pl.Float32,
        "mta_tax": pl.Float32,
        "tip_amount": pl.Float32,
        "tolls_amount": pl.Float32,
        "ehail_fee": pl.Float32,
        "improvement_surcharge": pl.Float32,
        "total_amount": pl.Float32,
        "payment_type": pl.Int32,
        "trip_type": pl.Int32,
        "congestion_surcharge": pl.Float32,
    }
)
csv_reader = pl.read_csv_batched(file_name, dtypes=dtypes)
```

If you run again at this stage, you should see the data types in the database change. Some integer fields go from BIGINT to INTEGER, which should use less memory.

### Renaming, Adding or Dropping Columns
We can easily add, remove or update columns in Polars. In fact, this can be done very efficiently by chaining the function calls together like so
```python
df
.rename({'a':'b'})
.with_columns([
    (pl.col("a").cast(pl.Date).alias("new_col_d")),
    (pl.col("b").cast(pl.Date).alias("new_col_e")),
])
.drop('c')
```

For us, we might want to rename columns to:
    (1) Give a friendly name that makes sense to us
    (2) Force all column names to use the correct format for Postgres - lower case with underscores. This has the added benefit that queries won't then need quotes around column names.

Wrt new columns, we could:
    (1) Create start and end date columns - since many of our queries use the datetime fields
    (2) Convert the flag field (which has "Y" & "N" entries) to a boolean
    (3) Use the dictionaries supplied in the [data dictionary](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf) to map to their corresponding text field

Here's what we could end up with
```python
rename_columns = {
    "VendorID": "vendor_id",
    "lpep_pickup_datetime": "start_datetime",
    "lpep_dropoff_datetime": "end_datetime",
    "RatecodeID": "rate_code_id",
    "PULocationID": "start_location_id",
    "DOLocationID": "end_location_id",
    "payment_type": "payment_type_id",
}

# Sourced from https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
rate_code_dict = {
    1: "Standard rate",
    2: "JFK",
    3: "Newark",
    4: "Nassau or Westchester",
    5: "Negotiated fare",
    6: "Group ride",
}

payment_type_dict = {
    1: "Credit card",
    2: "Cash",
    3: "No charge",
    4: "Dispute",
    5: "Unknown",
    6: "Voided trip",
}

new_columns = [
    (pl.col("start_datetime").cast(pl.Date).alias("start_date")),
    (pl.col("end_datetime").cast(pl.Date).alias("end_date")),
    (pl.col("store_and_fwd_flag").cast(pl.Boolean).alias("store_and_fwd_bool")),
    (pl.col("rate_code_id").replace(rate_code_dict).alias("rate_code")),
    (pl.col("payment_type_id").replace(payment_type_dict).alias("payment_type")),
]

drop_columns = ["store_and_fwd_flag"]

while (batches := csv_reader.next_batches(1)) is not None:
    time_start = time()
    record_counts = (
        batches[0]
        .rename(rename_columns)
        .with_columns(new_columns)
        .drop(drop_columns)
        .write_database(
            table_name=table_name,
            connection=connection,
            engine="adbc",
            if_table_exists=if_table_exists,
        )
    )
```

If we re-run again at this stage, we should see our new fields get created.

### Adding Schema/Config Data through Attached Volume

We could add a dictionary for each table within the main ingest_data_polars.py script, however, each time we wanted to change the data type, we would need to rebuild our image. Ideally we would avoid that since this is really meta data/configuration data and not application code. 

Instead we can pass a volume across when running the image. Within this folder, we can have add a schema.py file for each table. Any time we want to update the meta data within it, we can update the file directly. The next time the image is run, it will have access to the latest version of these files. Our new bash script should look like this:
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

Now in our main Polars script, we want to reference these files.
```python
import importlib
# Fetch the schema file for the corresponding table_name from the attached volume
schema = importlib.import_module("config.schema_" + table_name)
```

And in our polars functions, we reference the schema variable
```python
batches[0]
.rename(schema.rename_columns)
.with_columns(schema.new_columns)
.drop(schema.drop_columns)
.write_database(
    table_name=table_name,
    connection=connection,
    engine="adbc",
    if_table_exists=if_table_exists,
)
```

## Final Script
The final script can be found [here](ingest_data_polars.py)


## Further improvements
There are a number of further improvements I would like to make from this point:
(1) Improve configuration management
In the current implementation, our script would fail if we passed a table with no corresponding schema.py file. It would be nice to have a config management script setup with proper defaults for the necessary inputs. 
(2) Push postgres info to a config file
Similar to (1) above. Passing the host, port etc. is redundant.
(3) Use SOLID on main() function
Using SOLID principles (which are generally for OOP but can be applied to functional paradigm also) we could improve the flow in the main function. 
(4) Add Unit Testing
We could add unit tests to our functions after we have applied SOLID principles.