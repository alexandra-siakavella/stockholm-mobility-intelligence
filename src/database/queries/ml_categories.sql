SELECT
    transport_mode,
    COUNT(*) AS observations
FROM departure_ml_features
GROUP BY transport_mode
ORDER BY observations DESC;

SELECT
    line_designation,
    COUNT(*) AS observations
FROM departure_ml_features
GROUP BY line_designation
ORDER BY observations DESC;
