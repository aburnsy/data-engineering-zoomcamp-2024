from abc import ABC, abstractmethod
from dataclasses import dataclass
from polars import DataFrame
from typing import List
import logging
import pyarrow as pa
import pyarrow.parquet as pq
import asyncio
import aiohttp
import aiofile
import os


@dataclass
class DataSet:
    name: str
    curr_data: DataFrame
    table_name: str
    partition_keys: List[str] | None = None
    gcp_storage_path: str | None = None
    skip_publish: bool = False
    existing_data_behavior: str = "delete_matching"


class BaseETL(ABC):
    def __init__(self, root_gcp_storage_path: str = None, **kwargs):
        self.ROOT_GCP_STORAGE_PATH = (
            root_gcp_storage_path or "zoomcamp_week4_bigquery_andy_burns"
        )

    def validate_data(self, *args, **kwargs):
        pass

    def publish_dataset(self, input_data_set: DataSet):
        if not input_data_set.skip_publish:
            logging.info(f"Publishing {input_data_set.table_name}")
            curr_data = input_data_set.curr_data.to_arrow()
            gcs = pa.fs.GcsFileSystem()
            gcp_storage_path = (
                input_data_set.gcp_storage_path or input_data_set.table_name
            )
            pq.write_to_dataset(
                curr_data,
                root_path=f"{self.ROOT_GCP_STORAGE_PATH}/{gcp_storage_path}",
                partition_cols=input_data_set.partition_keys,
                filesystem=gcs,
                existing_data_behavior=input_data_set.existing_data_behavior,
            )

    @abstractmethod
    def get_bronze_dataset(self, **kwargs) -> DataSet:
        pass

    def get_silver_dataset(self, input_data_set: DataSet, **kwargs) -> DataSet:
        pass

    def get_gold_dataset(self, input_data_set: DataSet, **kwargs) -> DataSet:
        pass

    def run(self, **kwargs):
        bronze_data_set = self.get_bronze_dataset()
        self.validate_data(bronze_data_set)
        self.publish_dataset(bronze_data_set)
        logging.info("Imported, validated and published bronze data")

        silver_data_set = self.get_silver_dataset(bronze_data_set)
        self.validate_data(silver_data_set)
        self.publish_dataset(silver_data_set)
        logging.info("Imported, validated and published bronze data")

        gold_data_set = self.get_gold_dataset(silver_data_set)
        self.validate_data(gold_data_set)
        self.publish_dataset(gold_data_set)
        logging.info("Imported, validated and published gold data")

    def download_files(self, urls: list[any], folder_path: str = "downloads") -> None:
        os.makedirs(folder_path, exist_ok=True)
        sema = asyncio.BoundedSemaphore(6)

        async def fetch_file(session, url):
            fname = url.split("/")[-1]
            async with sema:
                async with session.get(url) as resp:
                    assert resp.status == 200
                    data = await resp.read()

            async with aiofile.async_open(
                os.path.join(folder_path, fname), "wb"
            ) as outfile:
                await outfile.write(data)
                unzip_file(os.path.join(folder_path, fname))

        def unzip_file(filename):
            is_gzipped = filename.split(".")[-1] == "gz"
            if is_gzipped:
                filename = filename[0:-3]

            if is_gzipped:
                os.system(f"gzip -d {filename}")

        async def main():
            async with aiohttp.ClientSession() as session:
                tasks = [fetch_file(session, url) for url in urls]
                await asyncio.gather(*tasks)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.close()
