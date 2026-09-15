select
    site_id,
    site_name,
    latitude,
    longitude,
    note,
    valid_from,
    case
        when latitude between 58.7 and 60.4
         and longitude between 17.2 and 19.2
        then true
        else false
    end as  within_stockholm_bbox

from {{ ref('stg_transport_sites') }}

