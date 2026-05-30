import os
import sys
import subprocess
from core.interfaces import QualityGateInterface

class PytestSubprocessValidator(QualityGateInterface):
    def verify(self, target_dir: str, test_filename: str) -> bool:
        print(f"\nStage 6: Running Automated Quality Verification Gates inside context '{target_dir}'...")
        print(f"Executing pytest suite on {test_filename}...")
        
        env = os.environ.copy()
        env["PYTHONPATH"] = os.path.abspath(target_dir)

        result = subprocess.run(
            [sys.executable, "-m", "pytest", test_filename, "-v"],
            capture_output=True,
            text=True,
            cwd=target_dir,
            env=env
        )
        
        if result.returncode == 0:
            print("Quality Gate Passed: All external unit tests executed successfully!")
            print(result.stdout)
            return True
        else:
            print("Quality Gate Failed: The generated feature code broke functional verification tests.")
            print("\n--- External Test Failure Output ---")
            print(result.stdout)
            print(result.stderr)
            return False