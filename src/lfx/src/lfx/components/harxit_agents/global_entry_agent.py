import os
from lfx.custom import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class HTGlobalEntryAgent(Component):
    display_name = "HT 38: Global Market Entry Agent"
    description: str = "Compliance and strategy for Dubai, USA, and Singapore markets."
    icon = "Globe"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="target_country", display_name="Target Market"),
    ]
    outputs = [
        Output(display_name="Entry Strategy", name="output", method="process"),
    ]

    def process(self) -> Message:
        api_key = self.groq_api_key or os.getenv("GROQ_API_KEY")
        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.1-8b-instant")
        
        prompt = (f"You are the Global Expansion Lead for Harxit Tech. For the following market and product info: {self.target_country}, "
                  "provide a 3-step entry strategy. Focus on: 1. Legal/Compliance (e.g. Dubai DED/DIFC), 2. High-ticket pricing strategy, 3. Cultural/Business localization.")
        
        response = llm.invoke(prompt)
        return Message(text=response.content)
