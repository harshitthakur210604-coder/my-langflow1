import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class PricingOptimizationAgent(Component):
    display_name: str = "HT 8: Pricing Optimization Agent"
    description: str = "Analyzes lead size and suggests Harxit Tech Pricing Tiers."
    name = "PricingOptimizationAgent"
    icon = "DollarSign"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="client_context", display_name="Client Context (Lead Data)"),
    ]

    outputs = [Output(display_name="Pricing Suggestion", name="output", method="suggest_pricing")]

    def suggest_pricing(self) -> Message:
        api_key = self.groq_api_key or os.getenv("GROQ_API_KEY")
        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.1-8b-instant")
        
        prompt = (f"Analyze this lead: {self.client_context}. \n\n"
                  "Based on the business type and potential, assign one of Harxit Tech's pricing tiers:\n"
                  "1. STARTER: ₹15,000 - ₹25,000 (Small shops, local clinics)\n"
                  "2. BUSINESS: ₹50,000 - ₹1,50,000 (Schools, Hotels, Real Estate)\n"
                  "3. ENTERPRISE: ₹5,00,000+ (Large SaaS, International Brands)\n\n"
                  "Provide the suggested tier and a short justification.")
        
        response = llm.invoke(prompt)
        return Message(text=response.content)
