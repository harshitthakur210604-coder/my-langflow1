import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class ReviewCollectorAgent(Component):
    display_name: str = "HT 22: Review Collector Agent"
    description: str = "Collects Google reviews and client feedback."
    name = "ReviewCollectorAgent"
    icon = "Star"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="project_outcome", display_name="Project Outcome"),
    ]

    outputs = [Output(display_name="Review Request", name="output", method="generate_request")]

    def generate_request(self) -> Message:
        api_key = self.groq_api_key

        if not api_key:

            api_key = os.getenv("GROQ_API_KEY")

        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.3-70b-versatile")
        prompt = (f"The project was successful: {self.project_outcome}. "
                  "Create a persuasive message asking the client for a Google review and detailed feedback.")
        response = llm.invoke(prompt)
        return Message(text=response.content)
