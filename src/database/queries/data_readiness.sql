SELECT
    COUNT(*) AS total_observations,
    COUNT(scheduled) AS observations_with_scheduled,
    COUNT(expected) AS observations_with_expected,
    COUNT(*) - COUNT(scheduled) AS missing_scheduled,
    COUNT(*) - COUNT(expected) AS missing_expected,
    COUNT(DISTINCT journey_id) AS unique_journeys
FROM departure_observations;
