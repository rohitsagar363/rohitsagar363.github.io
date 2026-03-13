from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
import random

import pandas as pd


SEVERITIES = ["MILD", "MODERATE", "SEVERE"]
OUTCOMES = ["RECOVERED", "RECOVERING", "ONGOING"]
VISIT_NAMES = ["SCREENING", "BASELINE", "WEEK_4", "WEEK_8", "WEEK_12"]
COUNTRIES = ["USA", "CAN", "GBR"]
THERAPEUTIC_AREAS = ["Oncology", "Immunology"]


@dataclass(frozen=True)
class SyntheticConfig:
    participant_count: int = 240
    seed: int = 42


def _site_lookup() -> pd.DataFrame:
    rows = [
        ("SITE_001", "Boston Clinical Research", "USA"),
        ("SITE_002", "Buffalo Medical Center", "USA"),
        ("SITE_003", "Toronto Health Network", "CAN"),
        ("SITE_004", "Seattle Trial Operations", "USA"),
        ("SITE_005", "London Translational Labs", "GBR"),
        ("SITE_006", "Austin Precision Research", "USA"),
    ]
    return pd.DataFrame(rows, columns=["site_id", "site_name", "country"])


def build_synthetic_sources(config: SyntheticConfig) -> dict[str, pd.DataFrame]:
    random.seed(config.seed)
    sites = _site_lookup()
    studies = pd.DataFrame(
        [
            ("STUDY_101", "Oncology", "Phase II"),
            ("STUDY_202", "Immunology", "Phase III"),
        ],
        columns=["study_id", "therapeutic_area", "phase"],
    )

    participant_rows = []
    visit_rows = []
    lab_rows = []
    adverse_event_rows = []

    base_date = date(2025, 1, 1)

    for idx in range(1, config.participant_count + 1):
        study_id = studies.iloc[idx % len(studies)]["study_id"]
        site = sites.iloc[idx % len(sites)]
        participant_id = f"PT_{idx:04d}"
        enrollment_date = base_date + timedelta(days=random.randint(0, 120))
        age = random.randint(21, 78)
        status = random.choices(
            ["ACTIVE", "ACTIVE", "ACTIVE", "SCREEN_FAILED", "COMPLETED"],
            weights=[45, 25, 10, 8, 12],
            k=1,
        )[0]
        sex = random.choice(["F", "M"])

        participant_rows.append(
            {
                "participant_id": participant_id,
                "study_id": study_id,
                "site_id": site["site_id"],
                "enrollment_date": enrollment_date.isoformat(),
                "age": age,
                "sex": sex,
                "status": status,
            }
        )

        visit_limit = 2 if status == "SCREEN_FAILED" else random.randint(3, 5)
        for visit_num, visit_name in enumerate(VISIT_NAMES[:visit_limit], start=1):
            visit_offset = max(0, (visit_num - 1) * 28 + random.randint(-2, 3))
            visit_date = enrollment_date + timedelta(days=visit_offset)
            completed = random.choices(["Y", "N"], weights=[92, 8], k=1)[0]
            visit_id = f"{participant_id}_{visit_name}"

            visit_rows.append(
                {
                    "visit_id": visit_id,
                    "participant_id": participant_id,
                    "visit_name": visit_name,
                    "visit_date": visit_date.isoformat(),
                    "completed_flag": completed,
                }
            )

            lab_rows.append(
                {
                    "lab_id": f"LAB_{participant_id}_{visit_num}",
                    "visit_id": visit_id,
                    "participant_id": participant_id,
                    "visit_date": visit_date.isoformat(),
                    "hemoglobin": round(random.uniform(9.2, 15.8), 1),
                    "alt_u_l": random.randint(18, 145),
                    "crp_mg_l": round(random.uniform(0.3, 18.0), 1),
                }
            )

        ae_count = random.choices([0, 1, 2], weights=[68, 24, 8], k=1)[0]
        for ae_num in range(ae_count):
            onset = enrollment_date + timedelta(days=random.randint(5, 90))
            adverse_event_rows.append(
                {
                    "event_id": f"AE_{participant_id}_{ae_num + 1}",
                    "participant_id": participant_id,
                    "event_term": random.choice(
                        ["FATIGUE", "NAUSEA", "HEADACHE", "ELEVATED_ALT", "RASH", "FEVER"]
                    ),
                    "severity": random.choices(SEVERITIES, weights=[58, 30, 12], k=1)[0],
                    "outcome": random.choice(OUTCOMES),
                    "onset_date": onset.isoformat(),
                }
            )

    participants = pd.DataFrame(participant_rows)
    visits = pd.DataFrame(visit_rows)
    labs = pd.DataFrame(lab_rows)
    adverse_events = pd.DataFrame(adverse_event_rows)

    return {
        "sites": sites,
        "studies": studies,
        "participants": participants,
        "visits": visits,
        "labs": labs,
        "adverse_events": adverse_events,
    }


def write_raw_sources(raw_dir: Path, config: SyntheticConfig) -> dict[str, Path]:
    raw_dir.mkdir(parents=True, exist_ok=True)
    tables = build_synthetic_sources(config)
    written: dict[str, Path] = {}
    for name, frame in tables.items():
        output = raw_dir / f"{name}.csv"
        frame.to_csv(output, index=False)
        written[name] = output
    return written
