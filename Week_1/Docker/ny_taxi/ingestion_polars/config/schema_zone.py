from collections import OrderedDict
import polars as pl

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


# df = csv_reader.next_batches(1)[0]
# for col, type in zip(df.columns, df.dtypes):
#     print(f'"{col}": pl.{type},')
