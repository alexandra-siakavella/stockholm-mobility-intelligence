CREATE OR REPLACE VIEW departure_ml_features AS

SELECT
    observation_id,
    site_id,
    journey_id,
    line_designation,
    transport_mode,
    destination,
    direction,

    observed_at,
    scheduled,

    EXTRACT(EPOCH FROM (scheduled - observed_at)) / 60.0
        AS minutes_until_departure,

    EXTRACT(HOUR FROM observed_at)
        AS observation_hour,

    EXTRACT(ISODOW FROM observed_at)
        AS observation_day_of_week,

    CASE
        WHEN EXTRACT(HOUR FROM observed_at) BETWEEN 7 AND 9
          OR EXTRACT(HOUR FROM observed_at) BETWEEN 16 AND 18
        THEN TRUE
        ELSE FALSE
    END AS is_peak_hour,

    delay_seconds

FROM departure_features
WHERE scheduled IS NOT NULL
  AND expected IS NOT NULL;
  