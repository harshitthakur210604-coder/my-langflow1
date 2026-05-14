import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class WhatsAppAutomationAgent(Component):
    display_name: str = "HT 10: WhatsApp Automation Agent"
    description: str = "Generates WhatsApp auto-replies and brochures."
    name = "WhatsAppAutomationAgent"
    icon = "MessageCircle"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="customer_message", display_name="Customer Message", info="What the customer sent on WhatsApp."),
    ]

    outputs = [Output(display_name="WhatsApp Response", name="output", method="generate_whatsapp_reply")]

    def generate_whatsapp_reply(self) -> Message:
        api_key = self.groq_api_key

        if not api_key:

            api_key = os.getenv("GROQ_API_KEY")

        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.3-70b-versatile")
        prompt = (f"The customer sent this on WhatsApp: '{self.customer_message}'. "
                  "Generate a friendly, helpful, and sales-oriented auto-reply. "
                  "Also, suggest a short brochure text to send alongside.")
        response = llm.invoke(prompt)
        return Message(text=response.content)
