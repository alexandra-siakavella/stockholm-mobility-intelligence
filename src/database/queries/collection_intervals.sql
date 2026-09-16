SELECT
    observed_at,
    COUNT(*) AS observations
FROM departure_observations
GROUP BY observed_at
ORDER BY observed_at;
