"""CLI entry point for the QA Testing Duo.

Usage examples (run from the project root):

    # Use a built-in sample story
    python main.py --sample shopping_cart

    # Provide your own story inline
    python main.py --story "As a user, I want to reset my password..."

    # Load a story from a file (txt, md, or json)
    python main.py --file samples/doctor_appointment.txt

Outputs are written to output/<run-name>/ as JSON, CSV and XLSX plus a
validation report.
"""

import argparse
import sys
from pathlib import Path

# CrewAI's verbose logger emits emoji; force UTF-8 so Windows consoles (cp1252)
# don't raise charmap encode errors while streaming agent logs.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from src.config import ConfigError, validate_config
from src.crew import PipelineError, run_pipeline
from src.exporters import write_all
from src.input_loader import InputError, load_story

ROOT = Path(__file__).parent
SAMPLES_DIR = ROOT / "samples"
OUTPUT_DIR = ROOT / "output"


def resolve_story(args) -> tuple[str, str]:
    """Return (story_text, run_name) from whichever input flag was used."""
    if args.sample:
        path = SAMPLES_DIR / f"{args.sample}.txt"
        if not path.exists():
            available = ", ".join(p.stem for p in SAMPLES_DIR.glob("*.txt"))
            raise InputError(
                f"Unknown sample '{args.sample}'. Available: {available or 'none'}"
            )
        return load_story(str(path)), args.sample
    if args.file:
        return load_story(args.file), Path(args.file).stem
    if args.story:
        return load_story(args.story, fmt="text"), "custom"
    raise InputError("Provide one of --sample, --file, or --story.")


def main() -> int:
    parser = argparse.ArgumentParser(description="QA Testing Duo (CrewAI + Gemini)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--sample", help="Name of a built-in sample (e.g. shopping_cart)")
    group.add_argument("--file", help="Path to a story file (.txt/.md/.json)")
    group.add_argument("--story", help="User story text provided inline")
    parser.add_argument(
        "--out",
        help="Output directory name (defaults to the run name under output/)",
    )
    args = parser.parse_args()

    try:
        validate_config()
        story, run_name = resolve_story(args)
    except (ConfigError, InputError) as exc:
        print(f"[input error] {exc}", file=sys.stderr)
        return 2

    print(f"Analyzing story '{run_name}' with the two-agent crew...\n")

    try:
        analysis, suite, report = run_pipeline(story)
    except PipelineError as exc:
        print(f"[pipeline error] {exc}", file=sys.stderr)
        return 1

    out_dir = OUTPUT_DIR / (args.out or run_name)
    written = write_all(analysis, suite, report, out_dir)

    print("\n=== Summary ===")
    print(f"Functional requirements : {len(analysis.functional_requirements)}")
    print(f"Non-functional reqs     : {len(analysis.non_functional_requirements)}")
    print(f"Edge cases              : {len(analysis.edge_cases)}")
    print(f"Gaps identified         : {len(analysis.gaps_identified)}")
    print(f"Test cases              : {len(suite.test_cases)}")
    print(f"Validation passed       : {report['overall_passed']}")
    print("\nArtifacts written:")
    for label, path in written.items():
        print(f"  - {label}: {path}")

    return 0 if report["overall_passed"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
