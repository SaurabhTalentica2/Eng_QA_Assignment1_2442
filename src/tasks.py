"""Task definitions for the QA Testing Duo.

Each task carries a detailed prompt and a Pydantic `output_pydantic` target so
CrewAI coerces the model output into a validated structure. The designer task
declares the analyst task as `context`, which is how requirements flow from the
first agent to the second.
"""

from crewai import Task

from .schemas import RequirementsAnalysis, TestSuite


def build_analysis_task(agent, user_story: str) -> Task:
    return Task(
        description=(
            "Analyze the following e-commerce user story (including any "
            "acceptance criteria) and extract a complete set of testable "
            "requirements.\n\n"
            "USER STORY AND ACCEPTANCE CRITERIA:\n"
            f"{user_story}\n\n"
            "Do all of the following:\n"
            "1. Extract FUNCTIONAL requirements (what the system must do). "
            "Assign IDs FR001, FR002, ... a priority (High/Medium/Low), a "
            "category, and whether it is testable.\n"
            "2. Extract NON-FUNCTIONAL requirements (performance, security, "
            "usability, reliability, persistence). Assign IDs NFR001, ... a "
            "type, and whether it is measurable.\n"
            "3. Identify EDGE CASES and boundary conditions. Assign IDs "
            "EC001, ... each with a description and the scenario that triggers "
            "it.\n"
            "4. Perform GAP ANALYSIS: list requirements that are ambiguous, "
            "missing, or conflicting (e.g. authentication, error handling, "
            "network failures) as short strings.\n\n"
            "Aim for at least 10 functional/non-functional requirements "
            "combined and at least 3 gaps. Be specific and testable; avoid "
            "restating the story verbatim. Echo the original story text back in "
            "the `user_story` field."
        ),
        expected_output=(
            "A JSON object with keys: user_story, functional_requirements, "
            "non_functional_requirements, edge_cases, gaps_identified."
        ),
        agent=agent,
        output_pydantic=RequirementsAnalysis,
    )


def build_design_task(agent, analysis_task) -> Task:
    return Task(
        description=(
            "Using the structured requirements produced by the Requirements "
            "Analyst, design a comprehensive test suite.\n\n"
            "Rules:\n"
            "- Produce 15 to 20 test cases total.\n"
            "- Cover POSITIVE (happy path), NEGATIVE (invalid input/error), "
            "BOUNDARY (limits such as max 10 items), and EDGE scenarios.\n"
            "- Every test case MUST reference the requirement it verifies via "
            "`requirement_id` (e.g. FR001, NFR001, EC001) for traceability.\n"
            "- Assign IDs TC001, TC002, ...\n"
            "- Give each case a title, type, priority, preconditions, the "
            "test_data needed, ordered steps, and the expected_result.\n"
            "- Include the original user story in the `user_story` field.\n"
        ),
        expected_output=(
            "A JSON object with keys: user_story and test_cases (a list of "
            "15-20 detailed test cases)."
        ),
        agent=agent,
        context=[analysis_task],
        output_pydantic=TestSuite,
    )
