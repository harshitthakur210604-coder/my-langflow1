import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class PaymentReminderAgent(Component):
    display_name: str = "HT 20: Payment Reminder Agent"
    description: str = "Sends automated reminders for due payments."
    name = "PaymentReminderAgent"
    icon = "Bell"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="client_name", display_name="Client Name"),
        MessageTextInput(name="amount_due", display_name="Amount Due"),
    ]

    outputs = [Output(display_name="Reminder Message", name="output", method="generate_reminder")]

    def generate_reminder(self) -> Message:
        api_key = self.groq_api_key

        if not api_key:

            api_key = os.getenv("GROQ_API_KEY")

        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.3-70b-versatile")
        prompt = (f"Create a polite but firm payment reminder for {self.client_name} regarding a due payment of {self.amount_due} to Harxit Tech.")
        response = llm.invoke(prompt)
        return Message(text=response.content)
