FROM python:3.11.8

RUN pip install polars pyarrow aiohttp aiofile

WORKDIR /app
COPY data_pipeline.py data_pipeline.py

ENTRYPOINT [ "python", "data_pipeline.py" ]