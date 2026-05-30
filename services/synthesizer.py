import os
from langchain_google_genai import ChatGoogleGenerativeAI
from core.interfaces import CodeSynthesizerInterface
from core.models import FeatureSpec, ImplementationPlan

class GeminiCodeSynthesizer(CodeSynthesizerInterface):
    def __init__(self, model_name: str = "gemini-2.5-flash", temperature: float = 0.1):
        self.llm = ChatGoogleGenerativeAI(model=model_name, temperature=temperature)

    def implement(self, plan: ImplementationPlan, spec: FeatureSpec, target_dir: str) -> str:
        chosen_filename = plan.impacted_files[0] if plan.impacted_files else "app.py"
        target_file_path = os.path.join(target_dir, chosen_filename)
        
        print(f"\nStage 4: AI Engine writing features to external file target: '{target_file_path}'...")
        
        existing_code = ""
        if os.path.exists(target_file_path):
            with open(target_file_path, "r") as f:
                existing_code = f.read()
        else:
            print(f"Target file '{chosen_filename}' doesn't exist yet. Bootstrapping raw project template from scratch.")

        clean_code = self._synthesize_source_code(plan, spec, existing_code)
        with open(target_file_path, "w") as f:
            f.write(clean_code)
        print(f"Changes successfully applied to external target file: {target_file_path}")

        test_filename = f"test_{chosen_filename}"
        test_file_path = os.path.join(target_dir, test_filename)
        print(f"Stage 5: Auto-generating test specifications inside target project ('{test_file_path}')...")
        
        clean_tests = self._synthesize_test_suite(plan, spec, chosen_filename, clean_code)
        with open(test_file_path, "w") as f:
            f.write(clean_tests)
        print(f"External test scenarios written to: {test_file_path}")
        
        return test_filename

    def _synthesize_source_code(self, plan: ImplementationPlan, spec: FeatureSpec, existing_code: str) -> str:
        prompt = f"""
        You are an expert Python Developer. Modify or create the base Python code to implement the new feature specification.
        CRITICAL INTERFACE CONTRACT CONSTRAINT: You MUST completely implement the exact architecture, global variables, classes, and methods mapped out in this codebase contract: {plan.codebase_contract}
        Existing Code Base Context: {existing_code}
        Target Feature Objectives: {spec.feature_objective}
        Acceptance Criteria: {spec.acceptance_criteria}
        Execution Strategy: {plan.technical_summary}
        Return ONLY valid, executable Python code. Do not wrap it in markdown block wrappers or conversational notes.
        """
        response = self.llm.invoke(prompt).content
        code_string = "".join([str(b) for b in response]) if isinstance(response, list) else str(response)
        return code_string.replace("```python", "").replace("```", "").strip()

    def _synthesize_test_suite(self, plan: ImplementationPlan, spec: FeatureSpec, chosen_filename: str, clean_code: str) -> str:
        module_name = os.path.splitext(chosen_filename)[0]
        prompt = f"""
        You are an expert QA Automation Engineer. Write a comprehensive suite of unit tests using the `pytest` framework for this code: {clean_code}
        CRITICAL STRUCTURAL VALIDATION REQUIREMENT: Your tests must strictly interface with the application using the components defined in this contract: {plan.codebase_contract}
        CRITICAL WINDOWS PATH COMPATIBILITY REQUIREMENT: When using `pytest.raises(..., match=...)` to match exceptions that mention paths, you MUST pass the string/path value through `re.escape()` to prevent regex compilation crashes caused by raw Windows backslashes (like '\\U').
        Example: `with pytest.raises(FileNotFoundError, match=re.escape(str(path))):`
        You must thoroughly verify all Acceptance Criteria scenarios: {spec.acceptance_criteria}
        CRITICAL: Ensure you include the correct import line to import classes/methods from the target file. (e.g., 'import {module_name}' or 'from {module_name} import ...')
        Return ONLY the valid executable Python code for the test suite. Do not wrap it in markdown blocks.
        """
        response = self.llm.invoke(prompt).content
        test_string = "".join([str(block) for block in response]) if isinstance(response, list) else str(response)
        return test_string.replace("```python", "").replace("```", "").strip()