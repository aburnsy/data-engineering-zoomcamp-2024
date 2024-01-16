FROM python:3.9

RUN pip install pandas

# Set cwd for container machine. All subsequent commands operate relative to here.
WORKDIR /app

# Name on the current server vs name on the container
COPY pipeline.py pipeline.py 

# Here we are overriding what was present in python dockerfile
ENTRYPOINT [ "python", "pipeline.py" ] 