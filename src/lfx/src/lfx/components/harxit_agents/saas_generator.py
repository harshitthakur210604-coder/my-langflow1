import os
from lfx.custom import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class HTSaaSGeneratorAgent(Component):
    display_name = "HT 37: SaaS Idea Generator"
    description: str = "Generating recurring revenue product ideas based on market niches."
    icon = "Lightbulb"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="market_niche", display_name="Market Niche"),
    ]
    outputs = [
        Output(display_name="SaaS Concept", name="output", method="process"),
    ]

    def process(self) -> Message:
        api_key = self.groq_api_key or os.getenv("GROQ_API_KEY")
        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.1-8b-instant")
        
        prompt = (f"You are the Lead Product Strategist at Harxit Tech. Based on this market data: {self.market_niche}, "
                  "design a specific AI SaaS product concept. Include: 1. Core Problem, 2. AI Feature, 3. Subscription Model (MRR Strategy).")
        
        response = llm.invoke(prompt)
        return Message(text=response.content)
