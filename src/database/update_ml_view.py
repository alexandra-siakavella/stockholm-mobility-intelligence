from sqlalchemy import create_engine, text


engine = create_engine(
    "postgresql+psycopg2://"
    "mobility_user:mobility_password@localhost:5432/mobility"
)

sql = """
DROP VIEW IF EXISTS departure_ml_features;

CREATE VIEW departure_ml_features AS

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
"""

with engine.begin() as connection:
    connection.execute(text(sql))

print("departure_ml_features view updated.")
