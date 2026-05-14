import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class SalesPitchAgent(Component):
    display_name: str = "HT 6: Sales Pitch Agent"
    description: str = "Generates high-conversion sales pitches with psychological triggers."
    name = "SalesPitchAgent"
    icon = "Megaphone"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="lead_report", display_name="Lead Report (from Flow 1)"),
        MessageTextInput(name="pricing_info", display_name="Pricing (from Agent 8)"),
    ]

    outputs = [Output(display_name="Final Sales Pitch", name="output", method="generate_pitch")]

    def generate_pitch(self) -> Message:
        api_key = self.groq_api_key or os.getenv("GROQ_API_KEY")
        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.3-70b-versatile")
        
        prompt = (f"LEAD DATA: {self.lead_report}\n"
                  f"PRICE QUOTE: {self.pricing_info}\n\n"
                  "Craft a high-conversion sales pitch for Harxit Tech. \n"
                  "1. Use 'Loss Aversion' (Explain what they are losing without a website).\n"
                  "2. Mention a limited-time 20% discount for this week.\n"
                  "3. Personalize it based on their category (School/Gym/etc).\n"
                  "4. Keep it short, bold, and ending with a question to start a chat.")
        
        response = llm.invoke(prompt)
        return Message(text=response.content)
