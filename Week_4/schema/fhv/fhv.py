from collections import OrderedDict
import polars as pl
from ..BaseETL import BaseETL, DataSet

dtypes = OrderedDict(
    {
        "LocationID": pl.Int32,
        "Borough": pl.Categorical,
        "Zone": pl.Categorical,
        "service_zone": pl.Categorical,
    }
)

rename_columns = {
    "LocationID": "location_id",
    "Borough": "borough",
    "Zone": "zone",
}

new_columns = []

drop_columns = []


class StandardETL(BaseETL):
    def get_bronze_dataset(self, **kwargs) -> DataSet:
        results = []
        for year in [2019, 2020]:
            for month in range(1, 13):
                url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_{year}-{str(month).zfill(2)}.csv.gz"
                csv_reader = pl.read_csv_batched(url, schema=dtypes)
                while (batches := csv_reader.next_batches(1)) is not None:
                    results.append(batches[0])
        return pl.concat(results)

    def get_gold_dataset(self, input_data_set: DataSet, **kwargs) -> DataSet:
        return input_data_set
