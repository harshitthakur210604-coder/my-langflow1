import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class ColdEmailAgent(Component):
    display_name: str = "HT 9: Cold Email Agent"
    description: str = "Generates high-converting cold email sequences."
    name = "ColdEmailAgent"
    icon = "Mail"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="target_niche", display_name="Target Niche", info="e.g., Schools in Agra"),
    ]

    outputs = [Output(display_name="Email Sequence", name="output", method="generate_emails")]

    def generate_emails(self) -> Message:
        api_key = self.groq_api_key

        if not api_key:

            api_key = os.getenv("GROQ_API_KEY")

        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.3-70b-versatile")
        prompt = (f"Create a 3-step cold email sequence (Day 1, Day 3, Day 7) for {self.target_niche}. "
                  "The emails should be short, provide value, and pitch Harxit Tech's digital services.")
        response = llm.invoke(prompt)
        return Message(text=response.content)
