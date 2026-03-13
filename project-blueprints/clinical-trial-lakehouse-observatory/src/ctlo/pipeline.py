from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import duckdb

from ctlo.config import ProjectPaths
from ctlo.quality import run_quality_checks
from ctlo.synthetic_data import SyntheticConfig, write_raw_sources


@dataclass
class PipelineResult:
    raw_files: dict[str, Path]
    gold_row_counts: dict[str, int]
    quality_issues: list[str]


def _clear_generated_files(paths: ProjectPaths) -> None:
    for directory in [paths.raw_dir, paths.bronze_dir, paths.silver_dir, paths.gold_dir]:
        if not directory.exists():
            continue
        for path in directory.iterdir():
            if path.is_file():
                path.unlink()


def _bronze_sql(paths: ProjectPaths) -> list[str]:
    return [
        f"copy (select * from read_csv_auto('{paths.raw_dir / 'sites.csv'}', header=true)) to '{paths.bronze_dir / 'sites.parquet'}' (format parquet)",
        f"copy (select * from read_csv_auto('{paths.raw_dir / 'studies.csv'}', header=true)) to '{paths.bronze_dir / 'studies.parquet'}' (format parquet)",
        f"copy (select * from read_csv_auto('{paths.raw_dir / 'participants.csv'}', header=true)) to '{paths.bronze_dir / 'participants.parquet'}' (format parquet)",
        f"copy (select * from read_csv_auto('{paths.raw_dir / 'visits.csv'}', header=true)) to '{paths.bronze_dir / 'visits.parquet'}' (format parquet)",
        f"copy (select * from read_csv_auto('{paths.raw_dir / 'labs.csv'}', header=true)) to '{paths.bronze_dir / 'labs.parquet'}' (format parquet)",
        f"copy (select * from read_csv_auto('{paths.raw_dir / 'adverse_events.csv'}', header=true)) to '{paths.bronze_dir / 'adverse_events.parquet'}' (format parquet)",
    ]


def _silver_sql(paths: ProjectPaths) -> list[str]:
    return [
        f"""
        copy (
            select
                participant_id,
                study_id,
                site_id,
                cast(enrollment_date as date) as enrollment_date,
                age,
                case when age < 35 then '18-34'
                     when age < 50 then '35-49'
                     when age < 65 then '50-64'
                     else '65+' end as age_band,
                sex,
                status
            from read_parquet('{paths.bronze_dir / 'participants.parquet'}')
        ) to '{paths.silver_dir / 'participants.parquet'}' (format parquet)
        """,
        f"""
        copy (
            select
                visit_id,
                participant_id,
                visit_name,
                cast(visit_date as date) as visit_date,
                completed_flag = 'Y' as visit_completed
            from read_parquet('{paths.bronze_dir / 'visits.parquet'}')
        ) to '{paths.silver_dir / 'visits.parquet'}' (format parquet)
        """,
        f"""
        copy (
            select
                lab_id,
                visit_id,
                participant_id,
                cast(visit_date as date) as visit_date,
                hemoglobin,
                alt_u_l,
                crp_mg_l,
                hemoglobin < 10.5 as low_hemoglobin_flag,
                alt_u_l > 80 as elevated_alt_flag,
                crp_mg_l > 10 as inflammation_flag
            from read_parquet('{paths.bronze_dir / 'labs.parquet'}')
        ) to '{paths.silver_dir / 'labs.parquet'}' (format parquet)
        """,
        f"""
        copy (
            select
                event_id,
                participant_id,
                upper(event_term) as event_term,
                upper(severity) as severity,
                upper(outcome) as outcome,
                cast(onset_date as date) as onset_date
            from read_parquet('{paths.bronze_dir / 'adverse_events.parquet'}')
        ) to '{paths.silver_dir / 'adverse_events.parquet'}' (format parquet)
        """,
        f"""
        copy (
            select *
            from read_parquet('{paths.bronze_dir / 'sites.parquet'}')
        ) to '{paths.silver_dir / 'sites.parquet'}' (format parquet)
        """,
        f"""
        copy (
            select *
            from read_parquet('{paths.bronze_dir / 'studies.parquet'}')
        ) to '{paths.silver_dir / 'studies.parquet'}' (format parquet)
        """,
    ]


def _gold_sql(paths: ProjectPaths) -> list[str]:
    return [
        f"""
        copy (
            select
                p.study_id,
                s.therapeutic_area,
                p.site_id,
                st.site_name,
                st.country,
                count(*) as enrolled_participants,
                sum(case when p.status = 'ACTIVE' then 1 else 0 end) as active_participants,
                sum(case when p.status = 'COMPLETED' then 1 else 0 end) as completed_participants
            from read_parquet('{paths.silver_dir / 'participants.parquet'}') p
            join read_parquet('{paths.silver_dir / 'studies.parquet'}') s using (study_id)
            join read_parquet('{paths.silver_dir / 'sites.parquet'}') st using (site_id)
            group by 1, 2, 3, 4, 5
            order by study_id, site_id
        ) to '{paths.gold_dir / 'gold_enrollment_site_summary.parquet'}' (format parquet)
        """,
        f"""
        copy (
            with latest_labs as (
                select *
                from (
                    select
                        participant_id,
                        visit_date,
                        hemoglobin,
                        alt_u_l,
                        crp_mg_l,
                        low_hemoglobin_flag,
                        elevated_alt_flag,
                        inflammation_flag,
                        row_number() over (partition by participant_id order by visit_date desc) as rn
                    from read_parquet('{paths.silver_dir / 'labs.parquet'}')
                )
                where rn = 1
            ),
            ae_counts as (
                select
                    participant_id,
                    count(*) as adverse_event_count,
                    sum(case when severity = 'SEVERE' then 1 else 0 end) as severe_event_count
                from read_parquet('{paths.silver_dir / 'adverse_events.parquet'}')
                group by 1
            )
            select
                p.participant_id,
                p.study_id,
                p.site_id,
                p.age_band,
                p.status,
                coalesce(ae.adverse_event_count, 0) as adverse_event_count,
                coalesce(ae.severe_event_count, 0) as severe_event_count,
                ll.hemoglobin,
                ll.alt_u_l,
                ll.crp_mg_l,
                case
                    when coalesce(ae.severe_event_count, 0) > 0 or ll.elevated_alt_flag then 'HIGH'
                    when ll.low_hemoglobin_flag or ll.inflammation_flag or coalesce(ae.adverse_event_count, 0) > 0 then 'MEDIUM'
                    else 'LOW'
                end as risk_bucket
            from read_parquet('{paths.silver_dir / 'participants.parquet'}') p
            left join latest_labs ll using (participant_id)
            left join ae_counts ae using (participant_id)
            order by participant_id
        ) to '{paths.gold_dir / 'gold_patient_risk_monitor.parquet'}' (format parquet)
        """,
        f"""
        copy (
            with visit_stats as (
                select
                    participant_id,
                    count(*) as visit_count,
                    sum(case when visit_completed then 1 else 0 end) as completed_visits
                from read_parquet('{paths.silver_dir / 'visits.parquet'}')
                group by 1
            ),
            risk_stats as (
                select
                    study_id,
                    count(*) as participants_monitored,
                    sum(case when risk_bucket = 'HIGH' then 1 else 0 end) as high_risk_participants,
                    sum(case when risk_bucket = 'MEDIUM' then 1 else 0 end) as medium_risk_participants
                from read_parquet('{paths.gold_dir / 'gold_patient_risk_monitor.parquet'}')
                group by 1
            )
            select
                p.study_id,
                s.therapeutic_area,
                count(distinct p.participant_id) as enrolled_participants,
                round(avg(v.visit_count), 2) as avg_visits_per_participant,
                round(avg(v.completed_visits), 2) as avg_completed_visits,
                rs.high_risk_participants,
                rs.medium_risk_participants
            from read_parquet('{paths.silver_dir / 'participants.parquet'}') p
            join read_parquet('{paths.silver_dir / 'studies.parquet'}') s using (study_id)
            left join visit_stats v using (participant_id)
            left join risk_stats rs using (study_id)
            group by 1, 2, 6, 7
            order by study_id
        ) to '{paths.gold_dir / 'gold_study_kpis.parquet'}' (format parquet)
        """,
    ]


def run_pipeline(paths: ProjectPaths, synthetic_config: SyntheticConfig) -> PipelineResult:
    paths.ensure_dirs()
    _clear_generated_files(paths)
    raw_files = write_raw_sources(paths.raw_dir, synthetic_config)
    conn = duckdb.connect()

    for statement in _bronze_sql(paths):
        conn.execute(statement)
    for statement in _silver_sql(paths):
        conn.execute(statement)
    for statement in _gold_sql(paths):
        conn.execute(statement)

    gold_row_counts = {
        "gold_enrollment_site_summary": conn.execute(
            f"select count(*) from read_parquet('{paths.gold_dir / 'gold_enrollment_site_summary.parquet'}')"
        ).fetchone()[0],
        "gold_patient_risk_monitor": conn.execute(
            f"select count(*) from read_parquet('{paths.gold_dir / 'gold_patient_risk_monitor.parquet'}')"
        ).fetchone()[0],
        "gold_study_kpis": conn.execute(
            f"select count(*) from read_parquet('{paths.gold_dir / 'gold_study_kpis.parquet'}')"
        ).fetchone()[0],
    }
    conn.close()

    issues = run_quality_checks(paths.silver_dir, paths.gold_dir)
    return PipelineResult(raw_files=raw_files, gold_row_counts=gold_row_counts, quality_issues=issues)
