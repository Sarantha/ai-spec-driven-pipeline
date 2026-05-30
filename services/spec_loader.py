import os
import json
import yaml
from core.interfaces import SpecLoaderInterface
from core.models import FeatureSpec

class YamlFeatureSpecLoader(SpecLoaderInterface):
    """Concrete execution strategy for parsing rigid PyYAML file formats."""
    def load(self, file_path: str) -> FeatureSpec:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not data or not isinstance(data, dict):
            raise ValueError("Target YAML file structure must map to a key-value dictionary schema.")
        return FeatureSpec(**data)


class JsonFeatureSpecLoader(SpecLoaderInterface):
    """Concrete execution strategy for parsing RFC-compliant structural JSON configurations."""
    def load(self, file_path: str) -> FeatureSpec:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not data or not isinstance(data, dict):
            raise ValueError("Target JSON file structure must map to a key-value object schema.")
        return FeatureSpec(**data)


class MarkdownFeatureSpecLoader(SpecLoaderInterface):
    """Concrete execution strategy for reading and ingesting free-form Markdown narratives."""
    def load(self, file_path: str) -> FeatureSpec:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_markdown = f.read().strip()
            
        if not raw_markdown:
            raise ValueError("Target Markdown specification file cannot be empty.")
            
        filename_title = os.path.splitext(os.path.basename(file_path))[0]
        
        # Build your custom FeatureSpec matching whatever fields your core models specify
        return FeatureSpec(
            feature_objective=f"Implement features described in {filename_title}",
            user_story="As a developer, I want to implement requirements defined within the Markdown document context.",
            business_rules=[f"System must respect constraints layout: {raw_markdown[:200]}..."],
            acceptance_criteria=[raw_markdown]
        )


class SpecLoaderFactory:
    """
    SOLID-Compliant Orchestrator Factory.
    Dynamically registers and provisions loaders based on physical file extensions.
    """
    _registry = {
        ".yaml": YamlFeatureSpecLoader,
        ".yml": YamlFeatureSpecLoader,
        ".json": JsonFeatureSpecLoader,
        ".md": MarkdownFeatureSpecLoader
    }

    @classmethod
    def get_loader(cls, file_path: str) -> SpecLoaderInterface:
        """
        Resolves the appropriate strategy class wrapper matching the specification format target.
        """
        ext = os.path.splitext(file_path)[1].lower()
        loader_class = cls._registry.get(ext)
        if not loader_class:
            raise ValueError(f"Unsupported file format extension encountered: '{ext}'")
        return loader_class()