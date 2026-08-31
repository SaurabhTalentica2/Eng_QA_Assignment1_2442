"""Output writers: JSON always, CSV/Excel for the test suite (bonus).

Kept separate from the crew so formats can be added without touching the
orchestration logic.
"""

import csv
import json
from pathlib import Path
from typing import Dict

from .schemas import RequirementsAnalysis, TestSuite


def write_json(obj, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = obj.model_dump() if hasattr(obj, "model_dump") else obj
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def write_test_cases_csv(suite: TestSuite, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "id",
        "title",
        "requirement_id",
        "type",
        "priority",
        "preconditions",
        "test_data",
        "steps",
        "expected_result",
    ]
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for tc in suite.test_cases:
            row = tc.model_dump()
            row["steps"] = " | ".join(row["steps"])  # flatten list for CSV
            writer.writerow(row)
    return path


def write_test_cases_excel(suite: TestSuite, path: Path) -> Path:
    """Export the suite to .xlsx. Requires openpyxl; degrades gracefully."""
    try:
        from openpyxl import Workbook
    except ImportError:
        return write_test_cases_csv(suite, path.with_suffix(".csv"))

    path.parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook()
    ws = wb.active
    ws.title = "Test Cases"
    headers = [
        "ID",
        "Title",
        "Requirement ID",
        "Type",
        "Priority",
        "Preconditions",
        "Test Data",
        "Steps",
        "Expected Result",
    ]
    ws.append(headers)
    for tc in suite.test_cases:
        ws.append(
            [
                tc.id,
                tc.title,
                tc.requirement_id,
                tc.type,
                tc.priority,
                tc.preconditions,
                tc.test_data,
                "\n".join(tc.steps),
                tc.expected_result,
            ]
        )
    wb.save(path)
    return path


def write_validation_report(report: Dict, path: Path) -> Path:
    return write_json(report, path)


def write_all(
    analysis: RequirementsAnalysis,
    suite: TestSuite,
    report: Dict,
    out_dir: Path,
) -> Dict[str, Path]:
    """Write every artifact and return the map of what was written."""
    return {
        "requirements": write_json(analysis, out_dir / "requirements.json"),
        "test_suite_json": write_json(suite, out_dir / "test_suite.json"),
        "test_suite_csv": write_test_cases_csv(suite, out_dir / "test_suite.csv"),
        "test_suite_xlsx": write_test_cases_excel(suite, out_dir / "test_suite.xlsx"),
        "validation_report": write_validation_report(
            report, out_dir / "validation_report.json"
        ),
    }
