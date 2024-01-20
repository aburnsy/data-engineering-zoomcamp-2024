#!/usr/bin/env python
# coding: utf-8
import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os


def main(params):
    time_starts = time()
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    # Get file information
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

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    # Setup the table
    df = pd.read_csv(file_name, nrows=0)
    if "lpep_pickup_datetime" in df.columns:
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    df.head(0).to_sql(name=table_name, con=engine, if_exists="replace")

    # Loop through all csv data
    df_iter = pd.read_csv(file_name, iterator=True, chunksize=200000)

    while (df := next(df_iter, None)) is not None:
        time_start = time()
        if "lpep_pickup_datetime" in df.columns:
            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

        df.to_sql(name=table_name, con=engine, if_exists="append")

        time_end = time()

        print(
            f"Inserted another chunk, taking {format(time_end-time_start,'.3f')} seconds"
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
