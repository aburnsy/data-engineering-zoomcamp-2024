import argparse
from importlib import import_module

if __name__ == "__main__":
    # Set up arguments and parse table name
    parser = argparse.ArgumentParser(
        description="Ingestion and transformation of Taxi data"
    )
    parser.add_argument("--dataset_name", help="Name of the dataset we are ingesting")
    args = parser.parse_args()
    dataset_name = args.dataset_name

    # import the schema for the
    schema = import_module("schema." + dataset_name)
    etl = schema.StandardETL()
    etl.run()
