# Original project blueprints for Rohith Sagar Karnala

These are the highest-value original projects to build next based on the reference repos and your background.

## 1. `clinical-trial-lakehouse-observatory`

### Positioning
Public demonstration of how to modernize a regulated batch platform into a governed lakehouse.

### Why it fits you
- directly reinforces Bristol Myers Squibb style work
- lets you showcase Iceberg or Delta patterns, governance, quality checks, and BI serving

### Core stack
- AWS S3
- PySpark
- Apache Iceberg or Delta Lake
- dbt
- Great Expectations or Soda
- Athena or DuckDB for querying
- Terraform

### Deliverables
- architecture diagram
- medallion or bronze/silver/gold layout
- synthetic clinical-trial dataset
- tests and data quality assertions
- cost and partitioning design notes
- dashboard screenshot

### Reference inspiration
- `streamify`
- `sql-data-warehouse-project`
- `pyspark-example-project`

## 2. `payer-claims-streaming-intelligence`

### Positioning
Real-time claims or member-event intelligence pipeline for healthcare operations.

### Why it fits you
- combines your healthcare domain depth with newer streaming skills
- differentiates you from batch-only data engineers

### Core stack
- Kafka or Redpanda
- Apache Flink or Spark Structured Streaming
- PostgreSQL
- dbt
- Grafana
- Docker Compose

### Deliverables
- synthetic claim, eligibility, or authorization events
- stream processing job with alerting or risk scoring
- warehouse tables for downstream reporting
- operational dashboard
- replayable local demo

### Reference inspiration
- `streamify`
- `data_engineering_best_practices`

## 3. `governed-support-analytics-platform`

### Positioning
Production-style async API ingestion and warehouse model for customer support analytics.

### Why it fits you
- extends your existing `talkdesk-async-etl` repo into a fuller platform
- shows ingestion, monitoring, warehouse modeling, and BI consumption in one repo

### Core stack
- Python `asyncio`
- `aiohttp`
- DuckDB or Postgres
- dbt
- lightweight dashboard or Evidence
- PyTest

### Deliverables
- rate-limited async extractor
- bronze raw landing tables
- silver normalized tables
- gold support KPI marts
- retry logic, monitoring, and data contract checks
- screenshots and benchmark notes

### Reference inspiration
- `josephmachado/data_engineering_best_practices`
- `pyspark-example-project`

## Publishing rule

For any project you publish:

1. use your own domain problem
2. change the architecture enough that it reflects your judgment
3. write original README, diagrams, and tradeoff notes
4. keep a short attribution note if a structure or template was inspired by a public repo
