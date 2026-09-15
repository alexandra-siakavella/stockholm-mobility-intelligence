SELECT
    line_designation,
    transport_mode,
    COUNT(*) AS observation_count,
    AVG(
        EXTRACT(
            EPOCH FROM (expected - scheduled)
        )
    ) AS average_delay_seconds,
    MAX(
        EXTRACT(
            EPOCH FROM (expected - scheduled)
        )
    ) AS maximum_delay_seconds
FROM departure_observations
WHERE scheduled IS NOT NULL
  AND expected IS NOT NULL
GROUP BY
    line_designation,
    transport_mode
ORDER BY
    average_delay_seconds DESC;
    