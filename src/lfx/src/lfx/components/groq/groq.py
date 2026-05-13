from pydantic.v1 import SecretStr

from lfx.base.models.groq_constants import GROQ_MODELS
from lfx.base.models.groq_model_discovery import get_groq_models
from lfx.base.models.model import LCModelComponent
from lfx.field_typing import LanguageModel
from lfx.field_typing.range_spec import RangeSpec
from lfx.io import (
    BoolInput, 
    DropdownInput, 
    IntInput, 
    MessageTextInput, 
    SecretStrInput, 
    SliderInput, 
    MessageInput, 
    HandleInput
)
from lfx.log.logger import logger

class GroqModel(LCModelComponent):
    display_name: str = "Groq (High-Speed)"
    description: str = "Generate high-speed text using Groq. Ideal for real-time AI agents and multilingual support (Hindi, etc.)."
    icon = "Groq"
    name = "GroqModel"

    inputs = [
        MessageInput(
            name="input_value", 
            display_name="Input", 
            info="The student's question.",
        ),
        HandleInput(
            name="system_message",
            display_name="System Message",
            info="The Teacher's rules and role.",
            input_types=["Message", "Text", "str", "Data", "Prompt"],
        ),
        BoolInput(
            name="stream", 
            display_name="Stream", 
            info="Stream the response text.", 
            advanced=True,
            value=True
        ),
        SecretStrInput(
            name="api_key",
            display_name="Groq API Key",
            info="API key for the Groq API. Get it from console.groq.com",
            real_time_refresh=True,
        ),
        MessageTextInput(
            name="base_url",
            display_name="Groq API Base",
            info="Base URL path for API requests.",
            advanced=True,
            value="https://api.groq.com",
            real_time_refresh=True,
        ),
        IntInput(
            name="max_tokens",
            display_name="Max Output Tokens",
            info="The maximum number of tokens to generate.",
            advanced=True,
        ),
        SliderInput(
            name="temperature",
            display_name="Temperature",
            value=0.1,
            info="Run inference with this temperature. Must by in the closed interval [0.0, 1.0].",
            range_spec=RangeSpec(min=0, max=1, step=0.01),
            advanced=True,
        ),
        IntInput(
            name="n",
            display_name="N",
            info="Number of chat completions to generate for each prompt.",
            advanced=True,
        ),
        DropdownInput(
            name="model_name",
            display_name="Model",
            info="The name of the model to use.",
            options=GROQ_MODELS,
            value=GROQ_MODELS[0],
            refresh_button=True,
            combobox=True,
        ),
        BoolInput(
            name="tool_model_enabled",
            display_name="Enable Tool Models",
            info="Select if you want to use models that can work with tools.",
            advanced=False,
            value=False,
            real_time_refresh=True,
        ),
    ]

    def get_models(self, *, tool_model_enabled: bool | None = None) -> list[str]:
        try:
            api_key = self.api_key if hasattr(self, "api_key") and self.api_key else None
            models_metadata = get_groq_models(api_key=api_key)
            model_ids = [
                model_id for model_id, metadata in models_metadata.items() if not metadata.get("not_supported", False)
            ]
            if tool_model_enabled:
                model_ids = [model_id for model_id in model_ids if models_metadata[model_id].get("tool_calling", False)]
            return model_ids or GROQ_MODELS
        except Exception:
            return GROQ_MODELS

    def update_build_config(self, build_config: dict, field_value: str, field_name: str | None = None):
        if field_name in {"base_url", "model_name", "tool_model_enabled", "api_key"} and field_value:
            try:
                ids = self.get_models(tool_model_enabled=self.tool_model_enabled)
                build_config.setdefault("model_name", {})
                build_config["model_name"]["options"] = ids
            except Exception as e:
                raise ValueError(f"Error getting model names: {e}") from e
        return build_config

    def build_model(self) -> LanguageModel:
        try:
            from langchain_groq import ChatGroq
        except ImportError as e:
            raise ImportError("Please install langchain-groq") from e

        api_key_value = SecretStr(self.api_key).get_secret_value() if self.api_key else None

        return ChatGroq(
            model=self.model_name,
            max_tokens=self.max_tokens or None,
            temperature=self.temperature,
            base_url=self.base_url,
            n=self.n or 1,
            api_key=api_key_value,
            streaming=self.stream,
        )
