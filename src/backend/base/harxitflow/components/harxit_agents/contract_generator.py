import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class ContractGeneratorAgent(Component):
    display_name: str = "HT 15: Contract Generator Agent"
    description: str = "Drafts legal service agreements and contracts."
    name = "ContractGeneratorAgent"
    icon = "ShieldCheck"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="project_scope", display_name="Project Scope"),
    ]

    outputs = [Output(display_name="Contract Draft", name="output", method="generate_contract")]

    def generate_contract(self) -> Message:
        api_key = self.groq_api_key

        if not api_key:

            api_key = os.getenv("GROQ_API_KEY")

        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.3-70b-versatile")
        prompt = (f"Draft a legal service agreement for Harxit Tech. Scope: {self.project_scope}. "
                  "Include standard clauses for payment, termination, confidentiality, and liability.")
        response = llm.invoke(prompt)
        return Message(text=response.content)
