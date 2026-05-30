import os
import sys
import argparse
from dotenv import load_dotenv

from core.interfaces import (
    SpecLoaderInterface, PlannerInterface, 
    CodeSynthesizerInterface, QualityGateInterface
)

from services.spec_loader import YamlFeatureSpecLoader
from services.planner import GeminiArchitectPlanner
from services.synthesizer import GeminiCodeSynthesizer
from services.validator import PytestSubprocessValidator

class PipelineOrchestrator:
    def __init__(
        self,
        loader: SpecLoaderInterface,
        planner: PlannerInterface,
        synthesizer: CodeSynthesizerInterface,
        validator: QualityGateInterface
    ):
        self.loader = loader
        self.planner = planner
        self.synthesizer = synthesizer
        self.validator = validator

    def run(self, spec_path: str, target_dir: str):
        spec_data = self.loader.load(spec_path)
        
        ai_plan = self.planner.design_plan(spec_data, target_dir)
        
        print("\n" + "="*50)
        print("DETAILED AI TECHNICAL BLUEPRINT GENERATED FOR EXTERNAL APP")
        print("="*50)
        print(f"Target Application Directory: {target_dir}")
        print(f"Plan Summary:\n{ai_plan.technical_summary}\n")
        print(f"Targeted Code Files to Alter: {ai_plan.impacted_files}\n")
        print("Operational Step-by-Step Tasks:")
        for idx, task in enumerate(ai_plan.tasks, 1):
            print(f"   {idx}. {task}")
        print("="*50)

        user_approval = input("\nGOVERNANCE LOCK: Approve execution? (y/n): ")
        if user_approval.lower() != 'y':
            print("Pipeline safely halted by user. External files left unchanged.")
            sys.exit(0)

        target_test_file = self.synthesizer.implement(ai_plan, spec_data, target_dir)
        
        success = self.validator.verify(target_dir, target_test_file)
        
        if success:
            print(f"\nSUCCESS: Feature validated successfully inside '{target_dir}'!")
        else:
            sys.exit(1)


if __name__ == "__main__":
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Universal SOLID AI-Native Feature Engine CLI")
    parser.add_argument("--spec", type=str, default="sample_spec.yaml", help="Path to specification file")
    parser.add_argument("--target-dir", type=str, default="workspace", help="Path to project directory")
    args = parser.parse_args()

    target_spec_path = os.path.abspath(args.spec)
    target_project_dir = os.path.abspath(args.target_dir)

    if not os.path.exists(target_project_dir):
        print(f"Error: Target application directory does not exist at '{target_project_dir}'")
        sys.exit(1)

    orchestrator = PipelineOrchestrator(
        loader=YamlFeatureSpecLoader(),
        planner=GeminiArchitectPlanner(),
        synthesizer=GeminiCodeSynthesizer(),
        validator=PytestSubprocessValidator()
    )
    
    orchestrator.run(target_spec_path, target_project_dir)