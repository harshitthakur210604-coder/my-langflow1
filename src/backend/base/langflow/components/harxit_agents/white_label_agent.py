import os
from lfx.custom import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class HTWhiteLabelAgent(Component):
    display_name = "HT 36: White-Label Partner Agent"
    description: str = "Onboarding and managing reseller agencies for Harxit Tech services."
    icon = "Users"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="agency_details", display_name="Target Agency Info"),
    ]
    outputs = [
        Output(display_name="Partnership Proposal", name="output", method="process"),
    ]

    def process(self) -> Message:
        api_key = self.groq_api_key or os.getenv("GROQ_API_KEY")
        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.1-8b-instant")
        
        prompt = (f"You are the Head of Partnerships at Harxit Tech. Generate a professional White-Label Partnership Pitch for: {self.agency_details}. "
                  "Focus on: 1. Wholesale pricing model, 2. No-branding delivery, 3. Harxit Tech's automation excellence.")
        
        response = llm.invoke(prompt)
        return Message(text=response.content)
