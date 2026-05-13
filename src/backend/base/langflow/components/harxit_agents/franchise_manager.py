import os
from lfx.custom import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class HTFranchiseManagerAgent(Component):
    display_name = "HT 39: Affiliate & Franchise Manager"
    description: str = "Managing the Harxit-in-a-Box model and partner networks."
    icon = "Briefcase"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="franchise_model", display_name="Model Details"),
    ]
    outputs = [
        Output(display_name="Network Strategy", name="output", method="process"),
    ]

    def process(self) -> Message:
        api_key = self.groq_api_key or os.getenv("GROQ_API_KEY")
        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.1-8b-instant")
        
        prompt = (f"You are the Franchise Development Manager at Harxit Tech. Based on this expansion plan: {self.franchise_model}, "
                  "draft a 'Harxit-in-a-Box' Franchise offer. Include: 1. One-time Setup Fee, 2. Monthly Royalties (%), 3. Training & Support provided by Harxit Tech HQ.")
        
        response = llm.invoke(prompt)
        return Message(text=response.content)
