import os
import sys
import yaml
from pydantic import ValidationError
from core.interfaces import SpecLoaderInterface
from core.models import FeatureSpec

class YamlFeatureSpecLoader(SpecLoaderInterface):
    def load(self, file_path: str) -> FeatureSpec:
        print(f"🔄 Stage 1: Ingesting specification from '{file_path}'...")
        if not os.path.exists(file_path):
            print(f"❌ Error: Specification file not found at '{file_path}'")
            sys.exit(1)
            
        with open(file_path, "r") as file:
            parsed_data = yaml.safe_load(file)

        try:
            validated_spec = FeatureSpec(**parsed_data)
            print("✅ Stage 1 Success: Specification passed structural quality validation checks.")
            return validated_spec
        except ValidationError as e:
            print("\n❌ Quality Gate Failed: Specification document is invalid.")
            for error in e.errors():
                field_name = " -> ".join(str(loc) for loc in error['loc'])
                print(f"👉 Field Errors: [{field_name}] -> {error['msg']}")
            sys.exit(1)