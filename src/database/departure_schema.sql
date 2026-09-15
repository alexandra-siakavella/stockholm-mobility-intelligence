CREATE TABLE IF NOT EXISTS departure_observations (
    observation_id BIGSERIAL PRIMARY KEY,

    site_id BIGINT NOT NULL,

    observed_at TIMESTAMPTZ NOT NULL,

    journey_id BIGINT,
    journey_state TEXT,

    line_id BIGINT,
    line_designation TEXT,

    transport_mode TEXT,
    group_of_lines TEXT,

    destination TEXT,
    direction TEXT,
    direction_code INTEGER,

    scheduled TIMESTAMP,
    expected TIMESTAMP,

    state TEXT,

    stop_area_id BIGINT,
    stop_area_name TEXT,

    stop_point_id BIGINT,
    stop_point_name TEXT,

    display TEXT,
    transport_authority_id BIGINT,

    deviations JSONB
);