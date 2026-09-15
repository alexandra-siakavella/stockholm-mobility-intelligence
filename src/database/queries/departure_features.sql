CREATE OR REPLACE VIEW departure_features AS

SELECT
    observation_id,
    site_id,
    observed_at,
    journey_id,
    journey_state,
    line_id,
    line_designation,
    transport_mode,
    group_of_lines,
    destination,
    direction,
    scheduled,
    expected,
    state,

    EXTRACT(
        EPOCH FROM (expected - scheduled)
    ) AS delay_seconds,

    CASE
        WHEN journey_state = 'CANCELLED'
        THEN TRUE
        ELSE FALSE
    END AS is_cancelled,

    EXTRACT(
        EPOCH FROM (scheduled - observed_at)
    ) / 60.0 AS minutes_until_departure,

    EXTRACT(
        HOUR FROM observed_at
    ) AS observation_hour,

    EXTRACT(
        ISODOW FROM observed_at
    ) AS observation_day_of_week,

    CASE
        WHEN EXTRACT(
            HOUR FROM observed_at
        ) BETWEEN 7 AND 9
        THEN TRUE

        WHEN EXTRACT(
            HOUR FROM observed_at
        ) BETWEEN 16 AND 18
        THEN TRUE

        ELSE FALSE
    END AS is_peak_hour

FROM departure_observations

WHERE scheduled IS NOT NULL
  AND expected IS NOT NULL;
  