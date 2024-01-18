#!/usr/bin/env python
# coding: utf-8
import polars as pl
from time import time
import argparse
import os
import importlib


def main(params):
    time_starts = time()
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    schema_file = "config.schema_" + table_name

    # print(f"Loading Schema information for table {table_name}")
    schema = importlib.import_module(schema_file)

    base_file: str = url.split("/")[-1]
    is_gzipped = base_file.split(".")[-1] == "gz"
    if is_gzipped:
        file_name = base_file[0:-3]
    else:
        file_name = base_file

    # download the file
    os.system(f"curl -L0 {url} --Output {base_file}")
    if is_gzipped:
        os.system(f"gzip -d {base_file}")

    connection = f"postgresql://{user}:{password}@{host}:{port}/{db}"

    # Batch the csv file for reading later
    csv_reader = pl.read_csv_batched(
        file_name, dtypes=schema.dtypes, ignore_errors=True
    )

    # Read the first batch of data and overwrite existing database with this information
    time_start = time()
    record_counts = (
        csv_reader.next_batches(1)[0]
        .rename(schema.rename_columns)
        .with_columns(schema.new_columns)
        .write_database(
            table_name=table_name,
            connection=connection,
            engine="adbc",
            if_table_exists="replace",
        )
    )
    print(
        f"Inserted first chunk of {record_counts}, taking {format(time()-time_start,'.3f')} seconds"
    )

    # Loop through all csv data
    while (batches := csv_reader.next_batches(1)) is not None:
        time_start = time()
        record_counts = (
            batches[0]
            .rename(schema.rename_columns)
            .with_columns(schema.new_columns)
            .write_database(
                table_name=table_name,
                connection=connection,
                engine="adbc",
                if_table_exists="append",
            )
        )

        print(
            f"Inserted another chunk of {record_counts}, taking {format(time()-time_start,'.3f')} seconds"
        )
    print(f"Total Time Taken: {format(time()-time_starts,'.3f')} seconds")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")

    # CTRL + d -> allows you to create multiple cursors on the same line
    parser.add_argument("--user", help="user name for postgres")
    parser.add_argument("--password", help="password for postgres")
    parser.add_argument("--host", help="host name for postgres")
    parser.add_argument("--port", help="port for postgres")
    parser.add_argument("--db", help="database name for postgres")
    parser.add_argument(
        "--table_name", help="name of the table we will write results to"
    )
    parser.add_argument("--url", help="url of the csv file to import")

    args = parser.parse_args()

    main(args)
