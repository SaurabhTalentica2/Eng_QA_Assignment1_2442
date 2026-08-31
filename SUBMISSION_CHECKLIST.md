# Submission Checklist

## What's included in the submission zip (qa-testing-duo-submission.zip)
- [x] Working two-agent system (Requirements Analyst + Test Case Designer)
- [x] Source code (src/, main.py) - clean and commented
- [x] README.md - setup, usage, architecture, design rationale, limitations
- [x] DEMO_SCRIPT.md - script for the required demo video
- [x] requirements.txt - reproducible dependencies
- [x] .env.example - config template (NO real key)
- [x] Sample inputs (samples/)
- [x] Sample outputs for BOTH stories (output/) - requirements + test cases +
      validation reports, in JSON/CSV/XLSX

## Deliberately EXCLUDED from the zip
- .env  (contains your real Gemini API key - never submit this)
- venv/ (machine-specific, hundreds of MB)
- __pycache__/ and other caches

## Verified results (latest run on gemini-3.6-flash)
- Shopping cart : 10 requirements, 4 edge cases, 4 gaps, 16 test cases - PASSED
- Doctor apptmt : 13 requirements, 3 edge cases, 4 gaps, 16 test cases - PASSED
- Full traceability (every test case links to a requirement id)
- NOTE: counts vary slightly per run since the LLM is generative; every run is
  checked against the quality gates in validation_report.json.

## STILL TO DO BY YOU (cannot be automated)
1. RECORD THE DEMO VIDEO (5 min) using DEMO_SCRIPT.md. This is a required
   deliverable for Assignment 1.
2. Submit qa-testing-duo-submission.zip + the video.
3. (Recommended) Rotate your Gemini API key after submitting, since it was
   shared in chat: https://aistudio.google.com/app/apikey

## To re-run later
    cd C:\Users\saurabhsi\qa-testing-duo
    .\venv\Scripts\python.exe main.py --sample shopping_cart
