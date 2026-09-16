SELECT
    COUNT(*) AS total_observations,
    COUNT(*) FILTER (WHERE delay_seconds = 0) AS zero_delay,
    COUNT(*) FILTER (WHERE delay_seconds > 0) AS delayed,
    COUNT(*) FILTER (WHERE delay_seconds < 0) AS early,
    ROUND(AVG(delay_seconds)::numeric, 2) AS average_delay_seconds,
    ROUND(MIN(delay_seconds)::numeric, 2) AS minimum_delay_seconds,
    ROUND(MAX(delay_seconds)::numeric, 2) AS maximum_delay_seconds
FROM departure_ml_features;

