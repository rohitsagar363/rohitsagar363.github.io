from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    root: Path

    @property
    def raw_dir(self) -> Path:
        return self.root / "data" / "raw"

    @property
    def bronze_dir(self) -> Path:
        return self.root / "warehouse" / "bronze"

    @property
    def silver_dir(self) -> Path:
        return self.root / "warehouse" / "silver"

    @property
    def gold_dir(self) -> Path:
        return self.root / "warehouse" / "gold"

    def ensure_dirs(self) -> None:
        for path in [self.raw_dir, self.bronze_dir, self.silver_dir, self.gold_dir]:
            path.mkdir(parents=True, exist_ok=True)


def get_project_paths(project_root: Path | None = None) -> ProjectPaths:
    root = project_root or Path(__file__).resolve().parents[2]
    return ProjectPaths(root=root)
