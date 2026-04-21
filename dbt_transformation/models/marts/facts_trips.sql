{{ config(materialized='table') }}

with trips as (
    select * from {{ ref('stg_trip_data') }}
)

select
    rental_id,
    bike_id,
    start_station_id,
    end_station_id,
    duration_seconds,
    -- Simple transformation: Duration in minutes
    round(duration_seconds / 60, 2) as duration_minutes,
    rental_date
from trips