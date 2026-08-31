"""Pydantic models describing the structured output of both agents.

These models are used two ways:
1. As CrewAI task `output_pydantic` targets, so the LLM is guided to produce
   well-formed JSON.
2. As a validation layer after the run, to guarantee the final artifacts match
   the schema documented in the assignment PRD.
"""

from typing import List

from pydantic import BaseModel, Field


# --------------------------------------------------------------------------- #
# Requirements Analyst output
# --------------------------------------------------------------------------- #
class FunctionalRequirement(BaseModel):
    id: str = Field(..., description="Stable ID, e.g. FR001")
    description: str = Field(..., description="What the system must do")
    priority: str = Field(..., description="High | Medium | Low")
    category: str = Field(..., description="e.g. Core Functionality, Cart, Auth")
    testable: bool = Field(..., description="Whether this can be directly tested")


class NonFunctionalRequirement(BaseModel):
    id: str = Field(..., description="Stable ID, e.g. NFR001")
    description: str
    type: str = Field(..., description="Performance | Security | Usability | ...")
    measurable: bool = Field(..., description="Whether it has a measurable target")


class EdgeCase(BaseModel):
    id: str = Field(..., description="Stable ID, e.g. EC001")
    description: str
    scenario: str = Field(..., description="Concrete situation that triggers it")


class RequirementsAnalysis(BaseModel):
    """Full output of the Requirements Analyst agent."""

    user_story: str
    functional_requirements: List[FunctionalRequirement] = Field(default_factory=list)
    non_functional_requirements: List[NonFunctionalRequirement] = Field(
        default_factory=list
    )
    edge_cases: List[EdgeCase] = Field(default_factory=list)
    gaps_identified: List[str] = Field(default_factory=list)


# --------------------------------------------------------------------------- #
# Test Case Designer output
# --------------------------------------------------------------------------- #
class TestCase(BaseModel):
    id: str = Field(..., description="Stable ID, e.g. TC001")
    title: str
    requirement_id: str = Field(
        ..., description="ID of the requirement this covers (traceability)"
    )
    type: str = Field(..., description="Positive | Negative | Boundary | Edge")
    priority: str = Field(..., description="High | Medium | Low")
    preconditions: str
    test_data: str = Field(..., description="Data needed to execute the test")
    steps: List[str] = Field(..., description="Ordered execution steps")
    expected_result: str


class TestSuite(BaseModel):
    """Full output of the Test Case Designer agent."""

    user_story: str
    test_cases: List[TestCase] = Field(default_factory=list)
