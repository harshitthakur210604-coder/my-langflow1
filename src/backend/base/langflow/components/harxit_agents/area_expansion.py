import os
from lfx.custom.custom_component.component import Component
from lfx.io import (
    MessageTextInput,
    Output,
    SecretStrInput,
)
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class LocalExpansionAgent(Component):
    display_name: str = "HT 3: Local Area Expansion Agent"
    description: str = "Suggests geographic expansion paths for business growth."
    name = "LocalExpansionAgent"
    icon = "Map"

    inputs = [
        SecretStrInput(
            name="groq_api_key",
            display_name="Groq API Key",
            required=True,
        ),
        MessageTextInput(
            name="current_city",
            display_name="Current City",
            info="The city where you are currently targeting (e.g., Agra).",
        ),
    ]

    outputs = [
        Output(display_name="Expansion Strategy", name="expansion_output", method="suggest_expansion"),
    ]

    def suggest_expansion(self) -> Message:
        api_key = self.groq_api_key

        if not api_key:

            api_key = os.getenv("GROQ_API_KEY")

        llm = ChatGroq(
            api_key=SecretStr(api_key).get_secret_value(),
            model="llama-3.3-70b-versatile",
        )
        
        prompt = (
            f"Harxit Tech is currently operating in {self.current_city}. "
            "Suggest a step-by-step geographic expansion plan starting from this city to nearby hubs and then pan-India. "
            "Analyze logistics, market size, and proximity. "
            "Example: Agra -> Firozabad -> Mathura -> Delhi NCR. "
            "Provide reasoning for each step."
        )
        
        response = llm.invoke(prompt)
        return Message(text=response.content)
