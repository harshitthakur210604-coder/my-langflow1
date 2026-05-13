import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class AnalyticsAgent(Component):
    display_name: str = "HT 24: Analytics Agent"
    description: str = "Generates revenue, conversion, and growth reports."
    name = "AnalyticsAgent"
    icon = "BarChart"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="raw_data", display_name="Raw Business Data"),
    ]

    outputs = [Output(display_name="Analytics Report", name="output", method="generate_report")]

    def generate_report(self) -> Message:
        api_key = self.groq_api_key

        if not api_key:

            api_key = os.getenv("GROQ_API_KEY")

        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.3-70b-versatile")
        prompt = (f"Analyze this raw data: {self.raw_data}. "
                  "Generate a summary report for Harxit Tech showing revenue trends, conversion rates, and growth opportunities.")
        response = llm.invoke(prompt)
        return Message(text=response.content)
