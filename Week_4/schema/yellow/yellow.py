from collections import OrderedDict
import polars as pl
from ..BaseETL import BaseETL, DataSet

dtypes = OrderedDict(
    {
        "VendorID": pl.Int32,
        "lpep_pickup_datetime": pl.Datetime(time_unit="us", time_zone=None),
        "lpep_dropoff_datetime": pl.Datetime(time_unit="us", time_zone=None),
        "passenger_count": pl.Int32,
        "trip_distance": pl.Float32,
        "RatecodeID": pl.Int32,
        "store_and_fwd_flag": pl.Categorical,
        "PULocationID": pl.Int32,
        "DOLocationID": pl.Int32,
        "payment_type": pl.Int32,
        "fare_amount": pl.Float32,
        "extra": pl.Float32,
        "mta_tax": pl.Float32,
        "tip_amount": pl.Float32,
        "tolls_amount": pl.Float32,
        "improvement_surcharge": pl.Float32,
        "total_amount": pl.Float32,
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


class StandardETL(BaseETL):
    def get_bronze_dataset(self, **kwargs) -> DataSet:
        urls = [
            f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_{year}-{str(month).zfill(2)}.csv.gz"
            for year in [2019, 2020]
            for month in range(1, 2)
        ]

        # self.download_files(urls=urls, folder_path="/app/schema/downloads")
        results = []
        for year in [2019, 2020]:
            for month in range(1, 2):
                file_name = f"/app/schema/downloads/yellow_tripdata_{year}-{str(month).zfill(2)}.csv"
                csv_reader = pl.read_csv_batched(file_name, dtypes=dtypes)
                while (batches := csv_reader.next_batches(1)) is not None:
                    results.append(batches[0])

        return DataSet(
            name="Yellow Taxi Data",
            curr_data=pl.concat(results),
            table_name="yellow_bronze",
            skip_publish=True,
        )

    def get_silver_dataset(self, input_data_set: DataSet, **kwargs) -> DataSet:
        curr_data = (
            input_data_set.curr_data.rename(rename_columns)
            .with_columns(new_columns)
            .drop(drop_columns)
        )
        return DataSet(
            name="Yellow Taxi Data",
            curr_data=curr_data,
            table_name="yellow_silver",
            partition_keys=["start_date"],
            gcp_storage_path="",
            skip_publish=True,
        )

    def get_gold_dataset(self, input_data_set: DataSet, **kwargs) -> DataSet:
        return DataSet(
            name="Yellow Taxi Data",
            curr_data=input_data_set.curr_data,
            table_name="yellow_gold",
            partition_keys=["start_date"],
            gcp_storage_path="",
            skip_publish=True,
        )
