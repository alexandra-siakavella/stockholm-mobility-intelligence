CREATE TABLE IF NOT EXISTS transport_sites (
    site_id BIGINT PRIMARY KEY,
    gid BIGINT NOT NULL,
    site_name TEXT NOT NULL,
    note TEXT,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    valid_from TIMESTAMP NOT NULL
);
