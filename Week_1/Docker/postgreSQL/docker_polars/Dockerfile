FROM python:3.12.1

RUN pip install polars adbc_driver_manager adbc-driver-postgresql pyarrow

WORKDIR /app
COPY config config
COPY ingest_data_polars.py ingest_data_polars.py

ENTRYPOINT [ "python", "ingest_data_polars.py" ]