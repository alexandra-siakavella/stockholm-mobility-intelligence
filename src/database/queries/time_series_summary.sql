SELECT
    MIN(observed_at) AS earliest_observation,
    MAX(observed_at) AS latest_observation,
    COUNT(*) AS observation_count,
    COUNT(DISTINCT journey_id) AS unique_journeys,
    COUNT(DISTINCT line_designation) AS unique_lines,
    COUNT(DISTINCT site_id) AS unique_sites
FROM departure_observations;
