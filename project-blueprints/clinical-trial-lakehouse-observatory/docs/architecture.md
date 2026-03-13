# Architecture notes

## Bronze

Raw CSV extracts are generated synthetically and landed into the bronze zone as Parquet without business logic applied.

## Silver

The silver layer standardizes data types, adds derived attributes such as `age_band`, and introduces domain checks such as lab alert flags.

## Gold

The gold layer exposes:

- site-level enrollment and completion metrics
- participant risk monitoring for operations teams
- study-level KPIs for portfolio and BI reporting

## Why DuckDB

DuckDB keeps the project fully local and easy to run while still providing SQL-driven transformation steps over Parquet, which makes the project easy to review and demo.
