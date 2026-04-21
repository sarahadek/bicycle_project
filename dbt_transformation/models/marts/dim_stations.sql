{{ config(materialized='table') }}

with unique_stations as (
    -- Combine Start and End stations to get a master list
    select 
        start_station_id as station_id, 
        start_station_name as station_name 
    from {{ ref('stg_trip_data') }}
    
    union distinct
    
    select 
        end_station_id as station_id, 
        end_station_name as station_name 
    from {{ ref('stg_trip_data') }}
)

select *
from unique_stations
where station_id is not null