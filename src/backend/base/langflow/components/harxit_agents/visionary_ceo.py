import os
from lfx.custom import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class HTVisionaryCEOAgent(Component):
    display_name = "HT 40: Visionary CEO Agent"
    description: str = "Long-term 5-year goals and high-valuation exit strategies."
    icon = "TrendingUp"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="long_term_vision", display_name="Vision/Exit Strategy"),
    ]
    outputs = [
        Output(display_name="Legacy Roadmap", name="output", method="process"),
    ]

    def process(self) -> Message:
        api_key = self.groq_api_key or os.getenv("GROQ_API_KEY")
        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.1-8b-instant")
        
        prompt = (f"You are the Visionary CEO of Harxit Tech. Synthesize all previous ecosystem data into a 5-Year Exit & Valuation Roadmap: {self.long_term_vision}. "
                  "Final goal: $10M+ Valuation. Include: 1. Growth Milestones, 2. IP Protection (Patents/Trademarks), 3. Exit/IPO potential.")
        
        response = llm.invoke(prompt)
        return Message(text=f"--- HARXIT TECH OFFICIAL 5-YEAR VISIONARY ROADMAP ---\n\n{response.content}")
