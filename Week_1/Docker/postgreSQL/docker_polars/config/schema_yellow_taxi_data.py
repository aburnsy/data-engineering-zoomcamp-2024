from collections import OrderedDict
import polars as pl

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


# df = csv_reader.next_batches(1)[0]
# for col, type in zip(df.columns, df.dtypes):
#     print(f'"{col}": {type}')
