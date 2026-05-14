import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class AdsAgent(Component):
    display_name: str = "HT 27: Ads Agent"
    description: str = "Creates Facebook and Google Ads campaigns."
    name = "AdsAgent"
    icon = "Layout"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="campaign_goal", display_name="Campaign Goal"),
    ]

    outputs = [Output(display_name="Ad Copy & Strategy", name="output", method="generate_ads")]

    def generate_ads(self) -> Message:
        api_key = self.groq_api_key

        if not api_key:

            api_key = os.getenv("GROQ_API_KEY")

        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.3-70b-versatile")
        prompt = (f"Goal: {self.campaign_goal}. "
                  "Create 3 variations of Facebook/Google Ad copy for Harxit Tech. Suggest target audience and budget strategy.")
        response = llm.invoke(prompt)
        return Message(text=response.content)
