import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class RetentionAgent(Component):
    display_name: str = "HT 35: Retention Agent"
    description: str = "Strategies for long-term client retention and maintenance."
    name = "RetentionAgent"
    icon = "RefreshCcw"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="client_feedback", display_name="Client Satisfaction Level"),
    ]

    outputs = [Output(display_name="Retention Strategy", name="output", method="generate_retention_plan")]

    def generate_retention_plan(self) -> Message:
        api_key = self.groq_api_key or os.getenv("GROQ_API_KEY")
        # Forced model: llama-3.1-8b-instant
        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.1-8b-instant")
        
        # Detect location from previous node output
        loc = "India"
        currency = "INR (₹)"
        if "LOCATION: International" in str(self.client_feedback):
            loc = "International"
            currency = "USD ($)"

        prompt = (f"Client Feedback Data: {self.client_feedback}\n"
                  f"Location: {loc}\n"
                  f"Target Currency: {currency}\n\n"
                  "Design a 6-month retention strategy. "
                  f"CRITICAL: Since the location is {loc}, you MUST use {currency} for all pricing suggestions. "
                  "Never use $ for Indian clients. All packages must be in the target currency.")
        
        response = llm.invoke(prompt)
        return Message(text=response.content)
