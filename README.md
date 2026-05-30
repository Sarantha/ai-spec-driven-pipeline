# AI-Native Spec-Driven Development Pipeline Prototype

This prototype implements an automated, spec-driven engineering loop that ingests feature criteria, generates technical blueprints, enforces human governance, modifies code within a sandbox, and validates structural stability using automated quality gates.

## Architecture Overview
1. **Spec Intake & Validation (Pydantic / PyYAML):** Enforces rigid structural validation over incoming technical specifications before execution.
2. **AI Planning Layer (Gemini 2.5 Flash):** Translates product goals into deterministic task blueprints using structured data schemas.
3. **Human Governance Gate:** Intercepts pipeline progress, halting application modification until explicit engineer verification.
4. **Sandbox Execution Layer:** Modifies code files and writes matching `pytest` suites restricted to isolated targets.
5. **Quality Verification Gates:** Automatically runs the test runners inside localized subprocesses to verify runtime pass states.

## Setup & Local Execution

### Prerequisites
- Python 3.10+
- A Google AI Studio Free API Key

### Installation
1. Clone the repository layouts.
2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate