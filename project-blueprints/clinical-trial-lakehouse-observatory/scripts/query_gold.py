from __future__ import annotations

from pathlib import Path
import sys

import duckdb

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from ctlo.config import get_project_paths


def main() -> None:
    paths = get_project_paths(PROJECT_ROOT)
    conn = duckdb.connect()

    print("Study KPIs")
    print("-" * 40)
    print(
        conn.execute(
            f"""
            select *
            from read_parquet('{paths.gold_dir / 'gold_study_kpis.parquet'}')
            order by study_id
            """
        ).df()
    )

    print("\nTop patient risk signals")
    print("-" * 40)
    print(
        conn.execute(
            f"""
            select participant_id, study_id, site_id, adverse_event_count, severe_event_count, alt_u_l, risk_bucket
            from read_parquet('{paths.gold_dir / 'gold_patient_risk_monitor.parquet'}')
            order by
                case risk_bucket when 'HIGH' then 1 when 'MEDIUM' then 2 else 3 end,
                severe_event_count desc,
                alt_u_l desc
            limit 10
            """
        ).df()
    )

    conn.close()


if __name__ == "__main__":
    main()
