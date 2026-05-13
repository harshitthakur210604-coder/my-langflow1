import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class UpsellAgent(Component):
    display_name: str = "HT 23: Upsell Agent"
    description: str = "Suggests additional services to existing clients."
    name = "UpsellAgent"
    icon = "TrendingUp"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="current_service", display_name="Current Service", info="What service is the client already using?"),
    ]

    outputs = [Output(display_name="Upsell Pitch", name="output", method="generate_upsell")]

    def generate_upsell(self) -> Message:
        api_key = self.groq_api_key

        if not api_key:

            api_key = os.getenv("GROQ_API_KEY")

        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.3-70b-versatile")
        prompt = (f"Client is using: {self.current_service}. "
                  "Suggest an upsell (e.g., Website -> Mobile App, CRM -> AI Automation) with a strong business case for Harxit Tech.")
        response = llm.invoke(prompt)
        return Message(text=response.content)
