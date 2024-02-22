{{ config(materialized="view") }}

with
    tripdata as (
        select
            dispatching_base_num,
            cast(pickup_datetime as timestamp) as pickup_datetime,
            cast(dropoff_datetime as timestamp) as dropoff_datetime,
            pulocationid,
            dolocationid,
            sr_flag,
            affiliated_base_number
        from {{ source("staging", "fhv_tripdata") }}
    )

select
    {{
        dbt_utils.generate_surrogate_key(
            ["dispatching_base_num", "pickup_datetime", "dropoff_datetime"]
        )
    }} as tripid,

    dispatching_base_num,

    -- timestamps
    pickup_datetime,
    dropoff_datetime,

    {{ dbt.safe_cast("PUlocationID", api.Column.translate_type("integer")) }}
    as pickup_locationid,
    {{ dbt.safe_cast("DOlocationID", api.Column.translate_type("integer")) }}
    as dropoff_locationid,

    sr_flag,
    affiliated_base_number

from tripdata
WHERE extract(year from pickup_datetime) = 2019

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var("is_test_run", default=false) %} limit 100 {% endif %}
