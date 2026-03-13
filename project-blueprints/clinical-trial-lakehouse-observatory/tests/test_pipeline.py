from __future__ import annotations

from pathlib import Path
import sys

import duckdb

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from ctlo.config import get_project_paths
from ctlo.pipeline import run_pipeline
from ctlo.synthetic_data import SyntheticConfig


def test_pipeline_creates_gold_outputs() -> None:
    paths = get_project_paths(PROJECT_ROOT)
    result = run_pipeline(paths, SyntheticConfig(participant_count=80, seed=11))

    assert not result.quality_issues
    assert result.gold_row_counts["gold_enrollment_site_summary"] > 0
    assert result.gold_row_counts["gold_patient_risk_monitor"] == 80
    assert result.gold_row_counts["gold_study_kpis"] == 2

    conn = duckdb.connect()
    high_risk = conn.execute(
        f"""
        select count(*)
        from read_parquet('{paths.gold_dir / 'gold_patient_risk_monitor.parquet'}')
        where risk_bucket = 'HIGH'
        """
    ).fetchone()[0]
    conn.close()

    assert high_risk >= 1
