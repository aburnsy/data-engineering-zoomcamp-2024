## Docker & SQL

## Question 1. Data Loading
- `266,855 rows x 20 columns`


## Question 2. Data Transformation
- `139,370 rows`


## Question 3. Data Transformation
- `data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date`


## Question 4. Data Transformation
- `1 or 2`
```SQL
SELECT distinct vendor_id 
FROM mage.green_taxi
```
> SQL Used for Question

## Question 5. Data Transformation
- `4`
```python
def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    result = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
    if name != result:
        print (f"Transformed column from {name} to {result}")
    return result
```
> This function was used to transform any Camel Case columns to Snake Case.


## Question 6. Data Exporting
- 96
The actual value I see is 95.
```python
@data_loader
def load_from_google_cloud_storage(*args, **kwargs):
    
    gcs = pa.fs.GcsFileSystem()

    parq_data = pq.ParquetDataset(
        path_or_paths=root_path,
        partitioning=['lpep_pickup_date'],
        filesystem=gcs,
    )
    
    fragments = parq_data.fragments
    print (len(fragments))
```

