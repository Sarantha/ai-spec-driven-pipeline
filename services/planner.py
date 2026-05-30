import os
import sys
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from core.interfaces import PlannerInterface
from core.models import FeatureSpec, ImplementationPlan

class GeminiArchitectPlanner(PlannerInterface):
    def __init__(self, model_name: str = "gemini-2.5-flash", temperature: float = 0.1):
        self.model_name = model_name
        self.temperature = temperature

    def _get_codebase_inventory(self, target_dir: str) -> list[str]:
        try:
            files = [f for f in os.listdir(target_dir) if f.endswith('.py') and not f.startswith('test_')]
            return files if files else ["app.py"]
        except Exception as e:
            print(f"Error scanning target directory '{target_dir}': {e}")
            sys.exit(1)

    def design_plan(self, spec: FeatureSpec, target_dir: str) -> ImplementationPlan:
        print("\nStage 2: Scanning target codebase and passing context to AI Planning Layer...")
        if not os.environ.get("GOOGLE_API_KEY"):
            print("Error: GOOGLE_API_KEY environment variable is missing!")
            sys.exit(1)

        codebase_files = self._get_codebase_inventory(target_dir)
        llm = ChatGoogleGenerativeAI(model=self.model_name, temperature=self.temperature)
        structured_llm = llm.with_structured_output(ImplementationPlan)

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", (
                "You are an expert Principal Cloud Architect and Senior Software Engineer.\n"
                "Your task is to analyze a feature specification and generate a concrete technical plan.\n"
                "CRITICAL: You must choose the target code file exclusively from this list of available files in the target project directory: {files_inventory}.\n"
                "If none match or the list is generic, default to modifying or creating 'app.py'.\n\n"
                "You MUST explicitly map out the exact structural code interface contract inside your `codebase_contract` output property so the downstream developer and QA automation engines line up flawlessly."
            )),
            ("human", (
                "Here is the validated feature specification:\n\n"
                "Objective: {feature_objective}\n"
                "User Story: {user_story}\n"
                "Business Rules:\n{business_rules}\n"
                "Acceptance Criteria:\n{acceptance_criteria}"
            ))
        ])

        formatted_prompt = prompt_template.format_messages(
            files_inventory=", ".join(codebase_files),
            feature_objective=spec.feature_objective,
            user_story=spec.user_story,
            business_rules="\n".join([f"- {rule}" for rule in spec.business_rules]),
            acceptance_criteria="\n".join([f"- {ac}" for ac in spec.acceptance_criteria])
        )

        try:
            plan: ImplementationPlan = structured_llm.invoke(formatted_prompt)
            print("Stage 2 Success: AI architect has constructed a structured technical blueprint.")
            return plan
        except Exception as e:
            print(f"Error during AI planning orchestration: {e}")
            sys.exit(1)