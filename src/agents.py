"""Agent definitions for the QA Testing Duo.

Two specialists:
  * Requirements Analyst  - turns a user story into structured requirements.
  * Test Case Designer     - turns requirements into a concrete test suite.

Both share a single Gemini-backed LLM. Roles/goals/backstories follow the
assignment PRD so each agent behaves like a domain expert.
"""

from crewai import Agent

from .config import build_llm


def build_requirements_analyst(llm=None) -> Agent:
    """Senior business analyst with e-commerce domain expertise."""
    return Agent(
        role="Senior Business Analyst with E-commerce Domain Expertise",
        goal=(
            "Extract, analyze, and structure testable requirements from business "
            "documentation and user stories, and surface gaps or ambiguities."
        ),
        backstory=(
            "You have spent 12 years turning vague product asks into precise, "
            "testable requirements for e-commerce platforms. You instinctively "
            "separate functional behavior from non-functional qualities, spot "
            "boundary conditions, and flag anything a story leaves unsaid."
        ),
        llm=llm or build_llm(),
        verbose=True,
        allow_delegation=False,
    )


def build_test_case_designer(llm=None) -> Agent:
    """Test architect who designs comprehensive, automation-ready test cases."""
    return Agent(
        role="Test Architect",
        goal=(
            "Design a comprehensive suite of test cases from analyzed "
            "requirements, covering positive, negative, boundary, and edge "
            "scenarios with clear steps and test data."
        ),
        backstory=(
            "You are a test architect who has shipped test strategies for large "
            "online stores. You apply equivalence partitioning and boundary-value "
            "analysis by reflex, and you always trace each test back to the "
            "requirement it verifies so coverage is provable."
        ),
        llm=llm or build_llm(),
        verbose=True,
        allow_delegation=False,
    )
