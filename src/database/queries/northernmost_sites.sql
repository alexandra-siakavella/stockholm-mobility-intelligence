SELECT
    site_id,
    site_name,
    latitude,
    longitude
FROM transport_sites
ORDER BY latitude DESC
LIMIT 10;