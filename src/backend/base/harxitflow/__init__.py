"""HarxitFlow backwards compatibility layer.

This module provides backwards compatibility by forwarding imports from
harxitflow.* to lfx.* to maintain compatibility with existing code that
references the old harxitflow module structure.
"""

from harxitflow.helpers.windows_postgres_helper import configure_windows_postgres_event_loop

configure_windows_postgres_event_loop(source="package_init")

import importlib  # noqa: E402
import importlib.util  # noqa: E402
import sys  # noqa: E402
from types import ModuleType  # noqa: E402
from typing import Any  # noqa: E402


class HarxitFlowCompatibilityModule(ModuleType):
    """A module that forwards attribute access to the corresponding lfx module."""

    def __init__(self, name: str, lfx_module_name: str):
        super().__init__(name)
        self._lfx_module_name = lfx_module_name
        self._lfx_module = None

    def _get_lfx_module(self):
        """Lazily import and cache the lfx module."""
        if self._lfx_module is None:
            try:
                self._lfx_module = importlib.import_module(self._lfx_module_name)
            except ImportError as e:
                msg = f"Cannot import {self._lfx_module_name} for backwards compatibility with {self.__name__}"
                raise ImportError(msg) from e
        return self._lfx_module

    def __getattr__(self, name: str) -> Any:
        """Forward attribute access to the lfx module with caching."""
        lfx_module = self._get_lfx_module()
        try:
            attr = getattr(lfx_module, name)
        except AttributeError as e:
            msg = f"module '{self.__name__}' has no attribute '{name}'"
            raise AttributeError(msg) from e
        else:
            # Cache the attribute in our __dict__ for faster subsequent access
            setattr(self, name, attr)
            return attr

    def __dir__(self):
        """Return directory of the lfx module."""
        try:
            lfx_module = self._get_lfx_module()
            return dir(lfx_module)
        except ImportError:
            return []


def _setup_compatibility_modules():
    """Set up comprehensive compatibility modules for harxitflow.base imports."""
    # First, set up the base attribute on this module (harxitflow)
    current_module = sys.modules[__name__]

    # Define all the modules we need to support
    module_mappings = {
        # Core base module
        "harxitflow.base": "lfx.base",
        # Inputs module - critical for class identity
        "harxitflow.inputs": "lfx.inputs",
        "harxitflow.inputs.inputs": "lfx.inputs.inputs",
        # Schema modules - also critical for class identity
        "harxitflow.schema": "lfx.schema",
        "harxitflow.schema.data": "lfx.schema.data",
        "harxitflow.schema.serialize": "lfx.schema.serialize",
        # Template modules
        "harxitflow.template": "lfx.template",
        "harxitflow.template.field": "lfx.template.field",
        "harxitflow.template.field.base": "lfx.template.field.base",
        # Components modules
        "harxitflow.components": "lfx.components",
        "harxitflow.components.helpers": "lfx.components.helpers",
        "harxitflow.components.helpers.calculator_core": "lfx.components.helpers.calculator_core",
        "harxitflow.components.helpers.create_list": "lfx.components.helpers.create_list",
        "harxitflow.components.helpers.current_date": "lfx.components.helpers.current_date",
        "harxitflow.components.helpers.id_generator": "lfx.components.helpers.id_generator",
        "harxitflow.components.helpers.memory": "lfx.components.helpers.memory",
        "harxitflow.components.helpers.output_parser": "lfx.components.helpers.output_parser",
        "harxitflow.components.helpers.store_message": "lfx.components.helpers.store_message",
        # Individual modules that exist in lfx
        "harxitflow.base.agents": "lfx.base.agents",
        "harxitflow.base.chains": "lfx.base.chains",
        "harxitflow.base.data": "lfx.base.data",
        "harxitflow.base.data.utils": "lfx.base.data.utils",
        "harxitflow.base.document_transformers": "lfx.base.document_transformers",
        "harxitflow.base.embeddings": "lfx.base.embeddings",
        "harxitflow.base.flow_processing": "lfx.base.flow_processing",
        "harxitflow.base.io": "lfx.base.io",
        "harxitflow.base.io.chat": "lfx.base.io.chat",
        "harxitflow.base.io.text": "lfx.base.io.text",
        "harxitflow.base.langchain_utilities": "lfx.base.langchain_utilities",
        "harxitflow.base.memory": "lfx.base.memory",
        "harxitflow.base.models": "lfx.base.models",
        "harxitflow.base.models.google_generative_ai_constants": "lfx.base.models.google_generative_ai_constants",
        "harxitflow.base.models.openai_constants": "lfx.base.models.openai_constants",
        "harxitflow.base.models.anthropic_constants": "lfx.base.models.anthropic_constants",
        "harxitflow.base.models.aiml_constants": "lfx.base.models.aiml_constants",
        "harxitflow.base.models.aws_constants": "lfx.base.models.aws_constants",
        "harxitflow.base.models.groq_constants": "lfx.base.models.groq_constants",
        "harxitflow.base.models.novita_constants": "lfx.base.models.novita_constants",
        "harxitflow.base.models.ollama_constants": "lfx.base.models.ollama_constants",
        "harxitflow.base.models.sambanova_constants": "lfx.base.models.sambanova_constants",
        "harxitflow.base.models.cometapi_constants": "lfx.base.models.cometapi_constants",
        "harxitflow.base.prompts": "lfx.base.prompts",
        "harxitflow.base.prompts.api_utils": "lfx.base.prompts.api_utils",
        "harxitflow.base.prompts.utils": "lfx.base.prompts.utils",
        "harxitflow.base.textsplitters": "lfx.base.textsplitters",
        "harxitflow.base.tools": "lfx.base.tools",
        "harxitflow.base.vectorstores": "lfx.base.vectorstores",
    }

    # Create compatibility modules for each mapping
    for harxitflow_name, lfx_name in module_mappings.items():
        if harxitflow_name not in sys.modules:
            # Check if the lfx module exists
            try:
                spec = importlib.util.find_spec(lfx_name)
                if spec is not None:
                    # Create compatibility module
                    compat_module = HarxitFlowCompatibilityModule(harxitflow_name, lfx_name)
                    sys.modules[harxitflow_name] = compat_module

                    # Set up the module hierarchy
                    parts = harxitflow_name.split(".")
                    if len(parts) > 1:
                        parent_name = ".".join(parts[:-1])
                        parent_module = sys.modules.get(parent_name)
                        if parent_module is not None:
                            setattr(parent_module, parts[-1], compat_module)

                    # Special handling for top-level modules
                    if harxitflow_name == "harxitflow.base":
                        current_module.base = compat_module
                    elif harxitflow_name == "harxitflow.inputs":
                        current_module.inputs = compat_module
                    elif harxitflow_name == "harxitflow.schema":
                        current_module.schema = compat_module
                    elif harxitflow_name == "harxitflow.template":
                        current_module.template = compat_module
                    elif harxitflow_name == "harxitflow.components":
                        current_module.components = compat_module
            except (ImportError, ValueError):
                # Skip modules that don't exist in lfx
                continue

    # Handle modules that exist only in harxitflow (like knowledge_bases)
    # These need special handling because they're not in lfx yet
    harxitflow_only_modules = {
        "harxitflow.base.data.kb_utils": "harxitflow.base.data.kb_utils",
        "harxitflow.base.knowledge_bases": "harxitflow.base.knowledge_bases",
        "harxitflow.components.knowledge_bases": "harxitflow.components.knowledge_bases",
    }

    for harxitflow_name in harxitflow_only_modules:
        if harxitflow_name not in sys.modules:
            try:
                # Try to find the actual physical module file
                from pathlib import Path

                base_dir = Path(__file__).parent

                if harxitflow_name == "harxitflow.base.data.kb_utils":
                    kb_utils_file = base_dir / "base" / "data" / "kb_utils.py"
                    if kb_utils_file.exists():
                        spec = importlib.util.spec_from_file_location(harxitflow_name, kb_utils_file)
                        if spec is not None and spec.loader is not None:
                            module = importlib.util.module_from_spec(spec)
                            sys.modules[harxitflow_name] = module
                            spec.loader.exec_module(module)

                            # Also add to parent module
                            parent_module = sys.modules.get("harxitflow.base.data")
                            if parent_module is not None:
                                parent_module.kb_utils = module

                elif harxitflow_name == "harxitflow.base.knowledge_bases":
                    kb_dir = base_dir / "base" / "knowledge_bases"
                    kb_init_file = kb_dir / "__init__.py"
                    if kb_init_file.exists():
                        spec = importlib.util.spec_from_file_location(harxitflow_name, kb_init_file)
                        if spec is not None and spec.loader is not None:
                            module = importlib.util.module_from_spec(spec)
                            sys.modules[harxitflow_name] = module
                            spec.loader.exec_module(module)

                            # Also add to parent module
                            parent_module = sys.modules.get("harxitflow.base")
                            if parent_module is not None:
                                parent_module.knowledge_bases = module

                elif harxitflow_name == "harxitflow.components.knowledge_bases":
                    components_kb_dir = base_dir / "components" / "knowledge_bases"
                    components_kb_init_file = components_kb_dir / "__init__.py"
                    if components_kb_init_file.exists():
                        spec = importlib.util.spec_from_file_location(harxitflow_name, components_kb_init_file)
                        if spec is not None and spec.loader is not None:
                            module = importlib.util.module_from_spec(spec)
                            sys.modules[harxitflow_name] = module
                            spec.loader.exec_module(module)

                            # Also add to parent module
                            parent_module = sys.modules.get("harxitflow.components")
                            if parent_module is not None:
                                parent_module.knowledge_bases = module
            except (ImportError, AttributeError):
                # If direct file loading fails, skip silently
                continue


# Set up all the compatibility modules
_setup_compatibility_modules()
