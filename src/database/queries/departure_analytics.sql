CREATE OR REPLACE VIEW departure_analytics AS
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
    direction_code,
    scheduled,
    expected,
    state,
    stop_area_id,
    stop_area_name,
    stop_point_id,
    stop_point_name,
    display,
    transport_authority_id,
    deviations,

    EXTRACT(
        EPOCH FROM (expected - scheduled)
    ) AS delay_seconds,

    CASE
        WHEN journey_state = 'CANCELLED'
        THEN TRUE
        ELSE FALSE
    END AS is_cancelled

FROM departure_observations
WHERE scheduled IS NOT NULL
  AND expected IS NOT NULL;