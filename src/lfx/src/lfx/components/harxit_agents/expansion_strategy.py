import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class ExpansionStrategyAgent(Component):
    display_name: str = "HT 30: Expansion Strategy Agent"
    description: str = "Suggests the next city or market for Harxit Tech expansion."
    name = "ExpansionStrategyAgent"
    icon = "Globe"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="current_market", display_name="Current Market Status"),
    ]

    outputs = [Output(display_name="Expansion Plan", name="output", method="generate_expansion")]

    def generate_expansion(self) -> Message:
        api_key = self.groq_api_key

        if not api_key:

            api_key = os.getenv("GROQ_API_KEY")

        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.3-70b-versatile")
        prompt = (f"Current Market: {self.current_market}. "
                  "Analyze the next best city/country for Harxit Tech to expand. Provide market research data and a step-by-step entry strategy.")
        response = llm.invoke(prompt)
        return Message(text=response.content)
