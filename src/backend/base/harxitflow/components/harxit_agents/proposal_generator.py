import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class ProposalGeneratorAgent(Component):
    display_name: str = "HT 14: Proposal Generator Agent"
    description: str = "Generates professional business proposals and quotations."
    name = "ProposalGeneratorAgent"
    icon = "FileText"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="client_needs", display_name="Client Needs"),
        MessageTextInput(name="pricing", display_name="Pricing Details"),
    ]

    outputs = [Output(display_name="Proposal Draft", name="output", method="generate_proposal")]

    def generate_proposal(self) -> Message:
        api_key = self.groq_api_key

        if not api_key:

            api_key = os.getenv("GROQ_API_KEY")

        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.3-70b-versatile")
        prompt = (f"Generate a professional business proposal for Harxit Tech. "
                  f"Client Requirements: {self.client_needs}. Pricing: {self.pricing}. "
                  "Include sections for Objectives, Solutions, Timeline, and Investment.")
        response = llm.invoke(prompt)
        return Message(text=response.content)
