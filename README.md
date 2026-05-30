# AI-Native Spec-Driven Development Pipeline Prototype

This prototype implements an automated, spec-driven engineering loop that ingests feature criteria, generates technical blueprints, enforces human governance, modifies code within an isolated sandbox directory, and validates structural stability using automated quality gates.

## Architecture Overview
1. **Spec Intake & Validation (Pydantic / PyYAML):** Enforces rigid structural validation over incoming technical specifications before execution begins.
2. **AI Planning Layer (Gemini 2.5 Flash):** Translates abstract product goals into deterministic task blueprints and code contracts using structured schema mapping.
3. **Human Governance Gate:** Intercepts pipeline progress, halting codebase modification until an explicit engineer verification/approval token is given.
4. **Sandbox Execution Layer:** Modifies target codebase scripts and constructs matching `pytest` suites restricted exclusively to isolated targets.
5. **Quality Verification Gates:** Automatically runs the test runners inside isolated localized subprocesses to verify runtime pass states before concluding.

## Repository Layout
```text
├── main.py               # CLI Orchestration Engine & Execution Kernel
├── ui.py                 # Streamlit UI Entry point & Coordinate Wrapper
├── .env                  # Local Private Keys & Environment Settings (Git Ignored)
├── .gitignore            # Git exclusion rules for environments, secrets, and caches
├── requirements.txt      # Project Third-Party Dependencies Module Tracker
│
├── core/                 # Abstract Enterprise Structural Contract Boundaries
│   ├── __init__.py       # Package Initialization
│   ├── interfaces.py     # ISP: Abstract Base Classes for loaders, planners, and synthesizers
│   └── models.py         # Data validation layers and schemas (FeatureSpec, ImplementationPlan)
│
├── services/             # Concrete Single-Responsibility Subsystems
│   ├── __init__.py
│   ├── spec_loader.py    # SRP: Ingests and validates PyYAML/Pydantic specifications
│   ├── planner.py        # SRP: Core AI Orchestrator compiling architectural blueprints
│   ├── synthesizer.py    # SRP: Handles targeted codebase mutations & automated test setups
│   └── validator.py      # SRP: Isolates shell subprocess testing execution contexts
│
└── ui/                   # Modularized UI Presentation Component Layer
    ├── __init__.py
    ├── components.py     # Clean isolated visual structural components (Headers, Shell frames)
    ├── styles.py         # Encapsulated premium dark-theme IDE-Aesthetic CSS codes
    └── utils.py          # Front-end helper tools & runtime stdout capturing traps

## Setup & Local Execution

Prerequisites
   Python 3.10+
   A Google AI Studio API Key

Installation & Environment Binding
   # Initialize virtual environment context
   python -m venv venv

   # Activate the environment shell
   # On Windows Command Prompt (cmd):
   venv\Scripts\activate
   # On Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   # On macOS / Linux:
   source venv/bin/activate

   # Upgrade pip package manager and install project requirements
   pip install --upgrade pip
   pip install -r requirements.txt

Configure Environment Keys
   GOOGLE_API_KEY=your_actual_google_ai_studio_api_key_here

Running the Application
   python -m streamlit run ui.py