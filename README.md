# Stockholm Mobility Intelligence

An end-to-end data engineering and machine learning project for collecting, validating, transforming, and analysing Stockholm public transport data.

The project explores how reliable data pipelines and machine learning can turn transport observations into useful mobility insights.

## Project Overview

The platform brings together several components of a data engineering workflow:

- **Data ingestion:** Collect and prepare public transport departure observations.
- **Data quality:** Validate critical fields and identify data-quality anomalies.
- **Data transformation:** Use dbt to support SQL-based data transformation and data modelling.
- **Data storage:** Work with PostgreSQL as part of the data platform.
- **Dataset preparation:** Split datasets for model development and evaluation.
- **Machine learning:** Train a delay prediction model and save evaluation metrics.
- **Automated testing:** Run Python tests locally and through GitHub Actions.

## Architecture

```text
Public Transport Observations
              |
              v
       Data Ingestion
              |
              v
       Data Validation
              |
              v
    PostgreSQL / Data Storage
              |
              v
      dbt Transformations
              |
              v
       Data Preparation
              |
              v
      Delay Prediction Model
              |
              v
     Model Evaluation Metrics
```

This illustrates the project's logical workflow; not every stage is necessarily orchestrated as a single automated pipeline.

## Technology Stack

- **Programming:** Python, SQL
- **Data processing:** pandas, NumPy
- **Data transformation:** dbt
- **Data validation:** Pydantic and custom data-quality checks
- **Database:** PostgreSQL
- **Machine learning:** scikit-learn, XGBoost
- **Database connectivity:** SQLAlchemy, psycopg2
- **Testing:** pytest
- **CI/CD:** GitHub Actions
- **Development environment:** Docker, GitHub Codespaces

## Data Ingestion and Quality

The project includes a departure data-collection pipeline and a quality-reporting module.

Run the data-quality report from the project root:

```bash
python -m src.quality.departure_quality
```

The report checks:

- Total number of observations
- Missing journey identifiers
- Missing scheduled and expected departure values
- Negative delay values
- Distinct sites and lines
- Earliest and latest observation timestamps

In the latest verified run, the report processed **2,174 observations**. It found no missing journey identifiers, scheduled departure values, or expected departure values, and identified three negative delays.

Negative delays are reported as potential anomalies rather than automatically removed.

## Data Transformation with dbt

dbt is part of the project's data transformation technology stack. It supports SQL-based transformation and modelling of data within the analytical workflow.

The aim is to make data transformations more maintainable, structured, and reproducible, creating a foundation for downstream analysis and reporting.

## Machine Learning

The project includes a delay prediction model and a saved preprocessing artifact.

Evaluation metrics are stored in `data/models/delay_model_metrics.csv`.

| Metric | Value |
|---|---:|
| Mean Absolute Error (MAE) | 75.48 |
| Root Mean Squared Error (RMSE) | 247.47 |

The target variable's unit and evaluation protocol should be confirmed before interpreting these values. A baseline comparison is also needed to establish whether the trained model improves on a simple prediction strategy.

Generated model artifacts are kept separate from the tracked evaluation metrics.

## Testing and Continuous Integration

Run the test suite from the project root:

```bash
python -m pytest -q
```

The latest verified local run passed **7 tests**.

A GitHub Actions workflow is configured to run tests on pushes and pull requests. Its successful completion should be verified through the GitHub Actions interface.

## Repository Structure

```text
.
├── .github/
│   └── workflows/
│       └── tests.yml
├── data/
│   └── models/
│       └── delay_model_metrics.csv
├── src/
│   ├── ingestion/
│   │   └── departures.py
│   ├── models/
│   │   └── split_dataset.py
│   ├── pipeline/
│   │   └── collect_departures.py
│   └── quality/
│       └── departure_quality.py
├── tests/
├── requirements.txt
└── README.md
```

This is a simplified view of the relevant project files.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/alexandra-siakavella/stockholm-mobility-intelligence.git
cd stockholm-mobility-intelligence
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the tests

```bash
python -m pytest -q
```

### 5. Run the data-quality report

```bash
python -m src.quality.departure_quality
```

Database-dependent and dbt workflows may require additional configuration.

## Roadmap

- Strengthen automated data-quality tests and anomaly handling.
- Improve documentation of dbt models, transformations, and data lineage.
- Establish a reproducible model evaluation protocol.
- Compare delay predictions against a baseline model.
- Improve pipeline orchestration and database integration.
- Add analytical outputs for transport performance and delay patterns.

## Project Status

The project is under active development, with a focus on reliable data processing, SQL-based transformation, reproducibility, data quality, and machine learning.