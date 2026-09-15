CREATE INDEX IF NOT EXISTS idx_departure_observed_at
ON departure_observations (observed_at);

CREATE INDEX IF NOT EXISTS idx_departure_line
ON departure_observations (line_designation);

CREATE INDEX IF NOT EXISTS idx_departure_journey
ON departure_observations (journey_id);

CREATE INDEX IF NOT EXISTS idx_departure_site_time
ON departure_observations (site_id, observed_at);
