## Rising Wave

## Question 0: What are the dropoff taxi zones at the latest dropoff times?
`Midtown Center`
```sql
CREATE MATERIALIZED VIEW latest_dropoff_times AS
    WITH t AS (
        SELECT MAX(tpep_dropoff_datetime) AS latest_dropoff_time
        FROM trip_data
    )
    SELECT taxi_zone.Zone as taxi_zone, latest_dropoff_time
    FROM t,
            trip_data
    JOIN taxi_zone
        ON trip_data.DOLocationID = taxi_zone.location_id
    WHERE trip_data.tpep_dropoff_datetime = t.latest_dropoff_time;
```

## Question 1: From this MV, find the pair of taxi zones with the highest average trip time.
`Yorkville East, Steinway`
```sql
CREATE MATERIALIZED VIEW zone_stats AS
    SELECT 
        pu_zone.Zone as pickup_zone, 
        do_zone.Zone as dropoff_zone, 
        avg(trip_data.tpep_dropoff_datetime - trip_data.tpep_pickup_datetime) as avg_time,
        min(trip_data.tpep_dropoff_datetime - trip_data.tpep_pickup_datetime) as min_time,
        max(trip_data.tpep_dropoff_datetime - trip_data.tpep_pickup_datetime) as max_time
    FROM trip_data
    JOIN taxi_zone pu_zone
        ON trip_data.PULocationID = pu_zone.location_id                 
    JOIN taxi_zone do_zone
        ON trip_data.DOLocationID = do_zone.location_id
    WHERE trip_data.PULocationID != trip_data.DOLocationID
    GROUP BY 
        pu_zone.Zone, do_zone.Zone
    ORDER BY 3 DESC;

SELECT * FROM zone_stats
LIMIT 1;
```


## Question 2: Find the number of trips for the pair of taxi zones with the highest average trip time.
`1`
```sql
CREATE MATERIALIZED VIEW zone_stats AS
    SELECT 
        pu_zone.Zone as pickup_zone, 
        do_zone.Zone as dropoff_zone, 
        avg(trip_data.tpep_dropoff_datetime - trip_data.tpep_pickup_datetime) as avg_time,
        min(trip_data.tpep_dropoff_datetime - trip_data.tpep_pickup_datetime) as min_time,
        max(trip_data.tpep_dropoff_datetime - trip_data.tpep_pickup_datetime) as max_time,
        count(1) as count
    FROM trip_data
    JOIN taxi_zone pu_zone
        ON trip_data.PULocationID = pu_zone.location_id                 
    JOIN taxi_zone do_zone
        ON trip_data.DOLocationID = do_zone.location_id
    WHERE trip_data.PULocationID != trip_data.DOLocationID
    GROUP BY 
        pu_zone.Zone, do_zone.Zone
    ORDER BY 3 DESC;

SELECT * FROM zone_stats
LIMIT 1;
```


## Question 3: From the latest pickup time to 17 hours before, what are the top 3 busiest zones in terms of number of pickups?
`LaGuardia Airport, Lincoln Square East, JFK Airport`
```sql
CREATE MATERIALIZED VIEW latest_17_hours_of_pickups AS
    WITH latest_pickup_time AS (
        SELECT MAX(tpep_pickup_datetime) AS latest_pickup_time
        FROM trip_data
    )
    SELECT 
        pu_zone.Zone as pickup_zone, 
        count(1) as count
    FROM trip_data
    JOIN taxi_zone pu_zone
        ON trip_data.PULocationID = pu_zone.location_id
    WHERE tpep_pickup_datetime > (SELECT latest_pickup_time - INTERVAL '17' HOUR FROM latest_pickup_time)
    GROUP BY 
        pu_zone.Zone
    ORDER BY 2 DESC, 1 DESC;

SELECT * FROM latest_17_hours_of_pickups
LIMIT 1;
```