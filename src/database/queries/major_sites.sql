SELECT
    site_id,
    site_name,
    latitude,
    longitude
FROM transport_sites
WHERE
    site_name ILIKE '%T-Centralen%'
    OR site_name ILIKE '%Slussen%'
    OR site_name ILIKE '%Odenplan%'
    OR site_name ILIKE '%Fridhemsplan%'
    OR site_name ILIKE '%Gullmarsplan%'
    OR site_name ILIKE '%Centralen%'
ORDER BY site_name;
