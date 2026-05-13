import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class DealClosingAgent(Component):
    display_name: str = "HT 7: Deal Closing Agent"
    description: str = "Handles objections and provides closing scripts."
    name = "DealClosingAgent"
    icon = "Gavel"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="objection", display_name="Client Objection", info="What is the client hesitant about? (e.g., Price is too high)"),
    ]

    outputs = [Output(display_name="Closing Strategy", name="output", method="handle_objection")]

    def handle_objection(self) -> Message:
        api_key = self.groq_api_key

        if not api_key:

            api_key = os.getenv("GROQ_API_KEY")

        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.3-70b-versatile")
        prompt = (f"The client has this objection: '{self.objection}'. "
                  "Provide a professional response to handle this objection and a final closing script to seal the deal for Harxit Tech. "
                  "Focus on value over cost.")
        response = llm.invoke(prompt)
        return Message(text=response.content)
