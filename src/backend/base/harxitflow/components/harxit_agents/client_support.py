import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class ClientSupportAgent(Component):
    display_name: str = "HT 21: Client Support Agent"
    description: str = "Provides automated support and handles client tickets."
    name = "ClientSupportAgent"
    icon = "LifeBuoy"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="client_issue", display_name="Client Issue"),
    ]

    outputs = [Output(display_name="Support Response", name="output", method="handle_issue")]

    def handle_issue(self) -> Message:
        api_key = self.groq_api_key

        if not api_key:

            api_key = os.getenv("GROQ_API_KEY")

        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.3-70b-versatile")
        prompt = (f"A client has this issue: '{self.client_issue}'. "
                  "Provide a supportive and technical response that resolves the issue professionally.")
        response = llm.invoke(prompt)
        return Message(text=response.content)
