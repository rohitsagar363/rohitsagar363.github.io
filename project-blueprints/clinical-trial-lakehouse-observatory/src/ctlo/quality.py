from __future__ import annotations

from pathlib import Path

import duckdb


def run_quality_checks(silver_dir: Path, gold_dir: Path) -> list[str]:
    issues: list[str] = []
    conn = duckdb.connect()

    duplicate_participants = conn.execute(
        f"""
        select count(*) from (
            select participant_id
            from read_parquet('{silver_dir / "participants.parquet"}')
            group by 1
            having count(*) > 1
        )
        """
    ).fetchone()[0]
    if duplicate_participants:
        issues.append(f"duplicate participants found: {duplicate_participants}")

    invalid_visit_dates = conn.execute(
        f"""
        select count(*)
        from read_parquet('{silver_dir / "visits.parquet"}') v
        join read_parquet('{silver_dir / "participants.parquet"}') p using (participant_id)
        where v.visit_date < p.enrollment_date
        """
    ).fetchone()[0]
    if invalid_visit_dates:
        issues.append(f"visits before enrollment found: {invalid_visit_dates}")

    unsupported_severity = conn.execute(
        f"""
        select count(*)
        from read_parquet('{silver_dir / "adverse_events.parquet"}')
        where severity not in ('MILD', 'MODERATE', 'SEVERE')
        """
    ).fetchone()[0]
    if unsupported_severity:
        issues.append(f"unsupported severity values found: {unsupported_severity}")

    empty_gold_tables = conn.execute(
        f"""
        select count(*) from (
            select 'gold_enrollment_site_summary' as table_name, count(*) as row_count
            from read_parquet('{gold_dir / "gold_enrollment_site_summary.parquet"}')
            union all
            select 'gold_patient_risk_monitor', count(*)
            from read_parquet('{gold_dir / "gold_patient_risk_monitor.parquet"}')
            union all
            select 'gold_study_kpis', count(*)
            from read_parquet('{gold_dir / "gold_study_kpis.parquet"}')
        ) where row_count = 0
        """
    ).fetchone()[0]
    if empty_gold_tables:
        issues.append(f"empty gold tables found: {empty_gold_tables}")

    conn.close()
    return issues
