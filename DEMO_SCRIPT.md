# 5-Minute Demo Script

Use this to record your screen-capture demo. Total ~5 minutes.

## 0:00 - 0:40  Intro
- "This is the E-commerce Testing Duo: a two-agent AI system built with CrewAI
  and Google Gemini."
- "Agent 1 is a Requirements Analyst; Agent 2 is a Test Case Designer. They run
  in a sequential CrewAI workflow: a user story goes in, structured requirements
  come out, and those requirements are handed to the designer which produces a
  full test suite."
- Show the project folder structure in the editor (src/ modules, samples/, README).

## 0:40 - 1:10  The two agents
- Open `src/agents.py`. Point out the two roles/goals/backstories.
- Open `src/tasks.py`. Show that the design task takes the analysis task as
  `context` - "this is how the requirements flow from agent 1 to agent 2."

## 1:10 - 2:40  Live run (shopping cart)
- In the terminal run:
    .\venv\Scripts\python.exe main.py --sample shopping_cart
- While it runs, narrate: "The analyst is extracting functional and
  non-functional requirements, edge cases, and gaps. Then the designer builds
  15-20 test cases."
- When it finishes, read out the summary (roughly 10 requirements, 3-4 edge
  cases, 4 gaps, ~16 test cases, validation passed - exact counts vary per run).

## 2:40 - 3:50  Show the output
- Open `output/shopping_cart/requirements.json` - show FRs, NFRs, edge cases,
  gaps_identified.
- Open `output/shopping_cart/test_suite.json` - show a couple of test cases with
  steps, test_data, expected_result, and the `requirement_id` traceability link.
- Open `output/shopping_cart/test_suite.xlsx` - "bonus: also exported to Excel."
- Open `output/shopping_cart/validation_report.json` - "every quality gate
  passes: 10+ requirements, 3+ gaps, 15-20 test cases, full traceability."

## 3:50 - 4:40  Second story + bonus
- Run:
    .\venv\Scripts\python.exe main.py --sample doctor_appointment
- "The same system handles a completely different, richer domain - a healthcare
  PRD - and correctly surfaces HIPAA, OAuth, and timezone requirements."
- Mention bonus features: multi-format input (txt / markdown / json),
  CSV + Excel export, traceability IDs, prioritization, validation report.

## 4:40 - 5:00  Wrap
- "Both agents collaborate through CrewAI's sequential process, outputs are
  schema-validated with Pydantic, and everything is documented in the README."
- Done.
