## Data Ingestion

## Question 1: What is the sum of the outputs of the generator for limit = 5?
- `C: 8.382332347441762`
```python
def square_root_generator(limit): 
    n = 1 
    while n <= limit: 
        yield n ** 0.5 
        n += 1 

running_sum = 0
generator = square_root_generator(5) 
for sqrt_value in generator: 
    running_sum += sqrt_value
print(running_sum)
```

## Question 2: What is the 13th number yielded by the generator?
- `B: 3.605551275463989`
```python
generator = square_root_generator(13) 
for sqrt_value in generator: 
    pass
print(sqrt_value)
```

## Question 3: Append the 2 generators. After correctly appending the data, calculate the sum of all ages of people.
- `A: 353`
```python
import dlt
import duckdb

people_pipeline = dlt.pipeline(destination='duckdb', dataset_name='people')

info = people_pipeline.run(people_1(), table_name='people', write_disposition='replace')
conn = duckdb.connect(f"{people_pipeline.pipeline_name}.duckdb")
conn.sql(f"SET search_path = '{people_pipeline.dataset_name}'")
display(conn.sql("SELECT sum(age) FROM people"))

info = people_pipeline.run(people_2(), table_name='people', write_disposition='append')
display(conn.sql("SELECT sum(age) FROM people"))
```

## Question 4: Merge the 2 generators using the ID column. Calculate the sum of ages of all the people loaded as described above
- `B: 266`
```python
import dlt

people_pipeline = dlt.pipeline(destination='duckdb', dataset_name='people')
people_pipeline.run(people_1(), table_name='people', write_disposition='replace', primary_key='ID')
people_pipeline.run(people_2(), table_name='people', write_disposition='merge', primary_key='ID')

conn = duckdb.connect(f"{people_pipeline.pipeline_name}.duckdb")
conn.sql(f"SET search_path = '{people_pipeline.dataset_name}'")
print(conn.sql("SELECT sum(age) FROM people"))
```