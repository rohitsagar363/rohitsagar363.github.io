# Reference repos for portfolio-grade data engineering projects

These repositories were selected as study material because they show strong architecture, documentation, and project packaging.

They should **not** be renamed and presented as original work. Use them to learn structure, testing, diagrams, and deployment patterns, then build differentiated projects around your own problem statements.

## Top picks

### 1. `ankurchavda/streamify`
- Link: https://github.com/ankurchavda/streamify
- Why it is strong:
  - end-to-end scope across Kafka, Spark Streaming, dbt, Airflow, Terraform, and GCP
  - includes architecture diagrams and workflow screenshots
  - shows how a streaming pipeline can still land in analytics-ready models
- What to borrow:
  - repo organization
  - infrastructure and orchestration separation
  - visual documentation style
- What not to copy:
  - music-streaming domain
  - exact DAGs, folder names, or transformation logic

### 2. `AlexIoannides/pyspark-example-project`
- Link: https://github.com/AlexIoannides/pyspark-example-project
- Why it is strong:
  - clean PySpark job structure
  - good testability and dependency packaging
  - concise example of how senior engineers organize ETL code
- What to borrow:
  - `configs/`, `dependencies/`, `jobs/`, `tests/` structure
  - separation of transformation logic from Spark session setup
  - testing style

### 3. `josephmachado/data_engineering_best_practices`
- Link: https://github.com/josephmachado/data_engineering_best_practices
- Why it is strong:
  - emphasizes engineering discipline rather than just tool demos
  - shows checks, local orchestration, and reproducibility
  - useful for improving the quality bar of your own repos
- What to borrow:
  - Makefile-driven workflows
  - repeatable local setup
  - quality and validation mindset

### 4. `DataWithBaraa/sql-data-warehouse-project`
- Link: https://github.com/DataWithBaraa/sql-data-warehouse-project
- Why it is strong:
  - strong documentation for warehouse layers, ETL, and data modeling
  - recruiter-friendly presentation
  - useful reference for how to explain medallion and star-schema work
- What to borrow:
  - documentation patterns
  - diagrams
  - data catalog and test folder ideas

## Cloned locally

The following repos are cloned into:

`/Users/rohithsagar/Documents/New project/references`

- `streamify`
- `pyspark-example-project`
- `data_engineering_best_practices`
- `sql-data-warehouse-project`

## Best path for your GitHub

Instead of copying public repos, build original projects in domains that match your background:

1. healthcare and payer analytics
2. governed lakehouse migrations
3. streaming recommendations or event intelligence
4. async API ingestion with observability and retries

Those will fit your resume and portfolio far better than generic Spotify or taxi-data clones.
