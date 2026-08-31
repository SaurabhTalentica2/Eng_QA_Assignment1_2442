"""Orchestration: wire the two agents into one sequential CrewAI workflow.

Flow:  user story -> Requirements Analyst -> Test Case Designer -> artifacts

`run_pipeline` is the single entry point used by the CLI and by tests. It
returns the validated analysis, the test suite, and a validation report.
"""

from typing import Dict, Tuple

from crewai import Crew, Process

from .agents import build_requirements_analyst, build_test_case_designer
from .config import build_llm
from .schemas import RequirementsAnalysis, TestSuite
from .tasks import build_analysis_task, build_design_task
from .validation import validate_analysis, validate_test_suite


class PipelineError(Exception):
    """Raised when the crew produces output that cannot be parsed."""


def build_crew(user_story: str) -> Tuple[Crew, object, object]:
    """Construct the crew and return it with its two tasks."""
    llm = build_llm()

    analyst = build_requirements_analyst(llm)
    designer = build_test_case_designer(llm)

    analysis_task = build_analysis_task(analyst, user_story)
    design_task = build_design_task(designer, analysis_task)

    crew = Crew(
        agents=[analyst, designer],
        tasks=[analysis_task, design_task],
        process=Process.sequential,
        verbose=True,
    )
    return crew, analysis_task, design_task


def run_pipeline(user_story: str) -> Tuple[RequirementsAnalysis, TestSuite, Dict]:
    """Run the full analyst -> designer workflow and validate the results."""
    if not user_story or not user_story.strip():
        raise PipelineError("A non-empty user story is required.")

    crew, analysis_task, design_task = build_crew(user_story)
    crew.kickoff()

    # Each task exposes its coerced Pydantic model via .output.pydantic.
    analysis = getattr(analysis_task.output, "pydantic", None)
    suite = getattr(design_task.output, "pydantic", None)

    if not isinstance(analysis, RequirementsAnalysis):
        raise PipelineError("Requirements analysis did not parse into the schema.")
    if not isinstance(suite, TestSuite):
        raise PipelineError("Test suite did not parse into the schema.")

    report = {
        "analysis": validate_analysis(analysis),
        "test_suite": validate_test_suite(suite, analysis),
    }
    report["overall_passed"] = (
        report["analysis"]["passed"] and report["test_suite"]["passed"]
    )
    return analysis, suite, report
