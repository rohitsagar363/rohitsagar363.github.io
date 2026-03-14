# Portfolio execution plan

## Exact GitHub pin strategy

Pin exactly four repositories.

1. `talkdesk-async-etl`
   - category: end-to-end logic
   - reason: strongest current proof of async ingestion, retries, API integration, monitoring, and gold outputs

2. `clinical-trial-lakehouse-observatory`
   - category: domain-shaped data platform
   - reason: strongest healthcare/pharma-aligned public repo and best fit for your resume signal

3. `governed-data-platform-infra` or `lakehouse-foundation-terraform`
   - category: environment management
   - status: missing, should be built next
   - target content: Terraform modules, environment overlays, IAM, storage, orchestration wiring, CI/CD, cost controls

4. `platform-ops-cli` or `data-engineering-toolkit`
   - category: development efficiency
   - status: missing, should be built after infra repo
   - target content: CLI for schema checks, local pipeline bootstrap, secrets templating, repo scaffolding, or dataset contract validation

Do not pin random forks or low-signal student projects just to fill the fourth slot.

## GitHub profile README

Create `rohitsagar363/rohitsagar363` with:

- one-sentence thesis
- current focus areas
- pinned repo descriptions
- short "engineering principles" section
- links to website, resume, and LinkedIn

Recommended opening thesis:

`I build governed data platforms for healthcare and pharma teams, with a focus on lakehouse modernization, reliability, cost control, and analyst-ready delivery.`

## Immediate repo improvements

Apply to all featured repos:

- add GitHub repo description
- add repo topics
- add `AI Use and Verification` section
- add CI badge and GitHub Actions workflow
- add `Architecture decisions` section
- add `Operational considerations` section
- add screenshots or table samples

## Suggested future projects

### 1. Governed data platform infra repo

Purpose:
- prove environment management, IaC discipline, and production thinking

Include:
- Terraform modules for storage, compute, IAM, secret handling, observability, and scheduler wiring
- separate `dev`, `stage`, `prod` overlays
- cost guardrails and tagging standards
- CI plan and drift strategy

### 2. Platform operations CLI

Purpose:
- prove developer-efficiency tooling and engineering ergonomics

Include:
- local project bootstrap
- pipeline contract validation
- schema diff utilities
- quality gate runner
- environment sanity checks

### 3. Open-source contribution track

Purpose:
- prove community alignment

Targets that fit your background:
- `dbt-core`
- `apache/airflow`
- `great-expectations`
- `soda-core`
- `dagster`
- `meltano`

Do not create a fake OSS repo for this. Earn it with real issues, docs, bug fixes, or plugin contributions.

### 4. Reliability-focused backend service

Purpose:
- strengthen backend and microservice credibility beyond data pipelines

Suggested repo:
- `claims-decisioning-api`

Include:
- rate limiting
- idempotency keys
- retries with jitter
- dead-letter handling
- tracing and metrics
- Postgres indexing notes

## Content artifacts to add

The portfolio should include:

- one ADR explaining a major architecture choice
- one postmortem or failure analysis
- one system design walkthrough
- explicit AI usage documentation

## What to do next

1. Fix GitHub pinning and profile README.
2. Add AI transparency to all featured repos.
3. Build the infra repo.
4. Build the platform CLI repo.
5. Earn one real open-source contribution and then pin it.
