#!/usr/bin/env python
# coding: utf-8
import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = "output.csv"

    # download the csv
    os.system(f"curl -L0 {url} --Output {csv_name}.gz")
    os.system(f"gzip -d {csv_name}.gz")

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    # Setup the table
    df = pd.read_csv(csv_name, nrows=0)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.head(0).to_sql(name=table_name, con=engine, if_exists="replace")

    # Loop through all csv data
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=200000)

    while (df := next(df_iter, None)) is not None:
        time_start = time()

        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name=table_name, con=engine, if_exists="append")

        time_end = time()

        print(
            f"Inserted another chunk, taking {format(time_end-time_start,'.3f')} seconds"
        )


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
