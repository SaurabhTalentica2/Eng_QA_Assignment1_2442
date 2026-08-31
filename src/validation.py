"""Post-run validation of agent outputs.

The Pydantic models already coerce shape during the crew run; this module adds
assignment-level quality gates (minimum counts, traceability integrity) and
returns a structured validation report rather than raising, so the report can be
saved alongside the outputs.
"""

from typing import Dict, List

from .schemas import RequirementsAnalysis, TestSuite


def validate_analysis(analysis: RequirementsAnalysis) -> Dict:
    """Check the requirements analysis against success criteria."""
    checks: List[Dict] = []

    total_reqs = len(analysis.functional_requirements) + len(
        analysis.non_functional_requirements
    )
    checks.append(
        {
            "check": "At least 10 testable requirements extracted",
            "passed": total_reqs >= 10,
            "actual": total_reqs,
        }
    )
    checks.append(
        {
            "check": "At least 3 gaps identified",
            "passed": len(analysis.gaps_identified) >= 3,
            "actual": len(analysis.gaps_identified),
        }
    )
    checks.append(
        {
            "check": "At least 1 edge case identified",
            "passed": len(analysis.edge_cases) >= 1,
            "actual": len(analysis.edge_cases),
        }
    )

    return {
        "component": "RequirementsAnalysis",
        "checks": checks,
        "passed": all(c["passed"] for c in checks),
    }


def validate_test_suite(suite: TestSuite, analysis: RequirementsAnalysis) -> Dict:
    """Check the test suite for coverage, count, and traceability integrity."""
    checks: List[Dict] = []

    count = len(suite.test_cases)
    checks.append(
        {
            "check": "15-20 test cases generated",
            "passed": 15 <= count <= 20,
            "actual": count,
        }
    )

    types = {tc.type.strip().lower() for tc in suite.test_cases}
    for needed in ("positive", "negative"):
        checks.append(
            {
                "check": f"Includes {needed} test cases",
                "passed": any(needed in t for t in types),
                "actual": sorted(types),
            }
        )

    # Traceability: every referenced requirement id should exist in the analysis.
    known_ids = (
        {r.id for r in analysis.functional_requirements}
        | {r.id for r in analysis.non_functional_requirements}
        | {e.id for e in analysis.edge_cases}
    )
    dangling = [
        tc.id
        for tc in suite.test_cases
        if tc.requirement_id and tc.requirement_id not in known_ids
    ]
    checks.append(
        {
            "check": "All test cases trace to a known requirement id",
            "passed": len(dangling) == 0,
            "actual": {"dangling_test_cases": dangling},
        }
    )

    return {
        "component": "TestSuite",
        "checks": checks,
        "passed": all(c["passed"] for c in checks),
    }
