from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from ctlo.config import get_project_paths
from ctlo.pipeline import run_pipeline
from ctlo.synthetic_data import SyntheticConfig


def main() -> None:
    paths = get_project_paths(PROJECT_ROOT)
    result = run_pipeline(paths, SyntheticConfig(participant_count=240, seed=42))

    print("Clinical Trial Lakehouse Observatory")
    print("=" * 40)
    print("Raw sources written:")
    for name, path in sorted(result.raw_files.items()):
        print(f"  - {name}: {path}")
    print("\nGold row counts:")
    for name, count in result.gold_row_counts.items():
        print(f"  - {name}: {count}")

    if result.quality_issues:
        print("\nQuality issues detected:")
        for issue in result.quality_issues:
            print(f"  - {issue}")
        raise SystemExit(1)

    print("\nQuality checks: passed")


if __name__ == "__main__":
    main()
