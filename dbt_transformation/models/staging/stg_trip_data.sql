{{ config(materialized='view') }}

with raw_data as (
    select * from {{ source('bicycle_source', 'stg_santander') }}
)

select
    -- renaming columns to match your schema:
    `Rental Id` as rental_id,
    Duration as duration_seconds,
    `Bike Id` as bike_id,
    
    -- MATCHING YOUR SCHEMA: 
    `StartStation Id` as start_station_id,
    `StartStation Name` as start_station_name,
    `EndStation Id` as end_station_id,
    `EndStation Name` as end_station_name,
    
    rental_date  -- Your partitioned column
from raw_data