import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class BillingFinanceAgent(Component):
    display_name: str = "HT 33: Billing & Finance Agent"
    description: str = "Manages invoicing and project cost analysis with multi-currency support."
    name = "BillingFinanceAgent"
    icon = "CreditCard"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="service_cost", display_name="Total Project Cost"),
    ]

    outputs = [Output(display_name="Invoice/Financial Report", name="output", method="generate_billing")]

    def generate_billing(self) -> Message:
        api_key = self.groq_api_key or os.getenv("GROQ_API_KEY")
        # Forced model: llama-3.1-8b-instant
        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.1-8b-instant")
        
        # Detect location from previous node output
        loc = "India"
        if "LOCATION: International" in str(self.service_cost):
            loc = "International"
            
        currency = "INR (₹)" if loc == "India" else "USD ($)"
        tax_info = "GST (18%)" if loc == "India" else "International Transaction Fees"
        
        prompt = (f"Project Cost: {self.service_cost}\n"
                  f"Detected Location: {loc}\n"
                  f"Target Currency: {currency}\n"
                  f"Tax Context: {tax_info}\n\n"
                  "Generate a professional invoice summary. "
                  f"CRITICAL: Since the location is {loc}, you MUST use {currency} and {tax_info}. "
                  "Never use $ for Indian clients. Show the total in the correct currency.")
        
        response = llm.invoke(prompt)
        loc_header = f"LOCATION: {loc}\n\n"
        return Message(text=loc_header + response.content)
