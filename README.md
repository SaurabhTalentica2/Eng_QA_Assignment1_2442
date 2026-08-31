# QA Testing Duo

A two-agent AI system built with **CrewAI** and **Google Gemini** that turns an
e-commerce user story into structured, testable requirements and then into a
comprehensive test suite.

```
user story  ->  Requirements Analyst  ->  Test Case Designer  ->  artifacts
                (structured JSON)          (15-20 test cases)      (json/csv/xlsx)
```

## Agents

| Agent | Role | Output |
|-------|------|--------|
| Requirements Analyst | Senior Business Analyst (e-commerce) | functional + non-functional requirements, edge cases, gap analysis |
| Test Case Designer | Test Architect | 15-20 positive/negative/boundary/edge test cases with traceability |

The two agents run as a **sequential CrewAI crew**. The designer receives the
analyst's structured output as task `context`, which is how requirements flow
from the first agent to the second.

## Project layout

```
qa-testing-duo/
  main.py                 CLI entry point (single command to run the whole flow)
  requirements.txt
  .env.example            copy to .env and add your Gemini key
  src/
    config.py             loads env + builds the shared Gemini LLM
    schemas.py            Pydantic models (RequirementsAnalysis, TestSuite)
    agents.py             the two agent definitions
    tasks.py              the two task definitions + prompts
    crew.py               orchestration (run_pipeline) - the integration layer
    validation.py         post-run quality gates + traceability check
    input_loader.py       multi-format input (text / markdown / json)
    exporters.py          JSON always, CSV + Excel for the test suite
  samples/
    shopping_cart.txt     the assignment's primary user story
    shopping_cart.json    same story in JSON (multi-format demo)
    doctor_appointment.txt richer PRD-based story for extra validation
  output/                 generated per-run artifacts (git-ignored)
```

## Setup

Requires **Python 3.10-3.13**.

```powershell
# 1. Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure your Gemini API key (free tier)
Copy-Item .env.example .env
# then edit .env and paste your key from https://aistudio.google.com/app/apikey
```

## Usage

```powershell
# Built-in sample (recommended first run)
python main.py --sample shopping_cart

# Richer PRD-based sample
python main.py --sample doctor_appointment

# Your own story inline
python main.py --story "As a user, I want to reset my password via email, so that I can regain access."

# From a file (.txt, .md, or .json)
python main.py --file samples/shopping_cart.json
```

Each run writes to `output/<run-name>/`:

- `requirements.json` - the analyst's structured output
- `test_suite.json` / `test_suite.csv` / `test_suite.xlsx` - the test cases
- `validation_report.json` - pass/fail against the success criteria

## Output schema

`requirements.json`:

```json
{
  "user_story": "...",
  "functional_requirements": [
    {"id": "FR001", "description": "...", "priority": "High",
     "category": "Core Functionality", "testable": true}
  ],
  "non_functional_requirements": [
    {"id": "NFR001", "description": "...", "type": "Performance",
     "measurable": true}
  ],
  "edge_cases": [
    {"id": "EC001", "description": "...", "scenario": "..."}
  ],
  "gaps_identified": ["..."]
}
```

`test_suite.json`:

```json
{
  "user_story": "...",
  "test_cases": [
    {"id": "TC001", "title": "...", "requirement_id": "FR001",
     "type": "Positive", "priority": "High", "preconditions": "...",
     "test_data": "...", "steps": ["..."], "expected_result": "..."}
  ]
}
```

Every test case carries a `requirement_id` for **traceability** back to a
specific requirement.

## Design decisions

- **Pydantic `output_pydantic`** on each task forces the LLM toward well-formed
  JSON and gives a validation layer for free.
- **Low temperature (0.2)** keeps extraction deterministic rather than creative.
- **Validation is a report, not an exception** - a run still produces artifacts
  even if a quality gate (e.g. exactly 15-20 cases) isn't met, so you can inspect
  what happened.
- **Exporters are decoupled** from the crew, so new formats don't touch
  orchestration.

## Bonus features implemented

- Multi-format input (plain text, markdown, JSON)
- Requirement prioritization (High/Medium/Low) and test-case prioritization
- Traceability IDs linking every test case to a requirement
- Test-case export to CSV and Excel
- Post-run validation report

## Known limitations

- Gemini free-tier rate limits can slow or throttle large runs; rerun if you hit
  a quota error.
- The LLM occasionally returns slightly fewer/more than 15-20 test cases; the
  validation report flags this rather than failing the run.
- No automated retry/backoff on transient API errors yet.
