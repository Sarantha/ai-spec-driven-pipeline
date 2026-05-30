from abc import ABC, abstractmethod
from typing import List
from .models import FeatureSpec, ImplementationPlan

class SpecLoaderInterface(ABC):
    @abstractmethod
    def load(self, file_path: str) -> FeatureSpec:
        pass

class PlannerInterface(ABC):
    @abstractmethod
    def design_plan(self, spec: FeatureSpec, target_dir: str) -> ImplementationPlan:
        pass

class CodeSynthesizerInterface(ABC):
    @abstractmethod
    def implement(self, plan: ImplementationPlan, spec: FeatureSpec, target_dir: str) -> str:
        pass

class QualityGateInterface(ABC):
    @abstractmethod
    def verify(self, target_dir: str, test_filename: str) -> bool:
        pass