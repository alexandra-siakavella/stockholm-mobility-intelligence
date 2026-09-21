import pandas as pd
from sqlalchemy import create_engine


engine = create_engine(
    "postgresql+psycopg2://"
    "mobility_user:mobility_password@localhost:5432/mobility"
)

query = """
SELECT
    journey_id,
    site_id,
    line_designation,
    observed_at,
    scheduled,
    delay_seconds
FROM departure_ml_features
WHERE journey_id IS NOT NULL
ORDER BY journey_id, observed_at;
"""

df = pd.read_sql(query, engine)

print("Rows with journey IDs:", len(df))
print("Unique journeys:", df["journey_id"].nunique())

journey_counts = df["journey_id"].value_counts()

print("\nObservations per journey:")
print(journey_counts.describe())

print("\nMost frequently observed journeys:")
print(journey_counts.head(10))
