import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class FollowUpAgent(Component):
    display_name: str = "HT 12: Follow-up Agent"
    description: str = "Auto reminders and follow-up messages for pending leads."
    name = "FollowUpAgent"
    icon = "Clock"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="lead_name", display_name="Lead Name"),
        MessageTextInput(name="last_interaction", display_name="Last Interaction", info="What was discussed last time?"),
    ]

    outputs = [Output(display_name="Follow-up Message", name="output", method="generate_followup")]

    def generate_followup(self) -> Message:
        api_key = self.groq_api_key

        if not api_key:

            api_key = os.getenv("GROQ_API_KEY")

        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.3-70b-versatile")
        prompt = (f"Lead: {self.lead_name}. Last talk: {self.last_interaction}. "
                  "Create a gentle yet firm follow-up message to remind them about our previous discussion and push for the next step.")
        response = llm.invoke(prompt)
        return Message(text=response.content)
