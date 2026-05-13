import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class CompetitorAnalysisAgent(Component):
    display_name: str = "HT 25: Competitor Analysis Agent"
    description: str = "Analyzes local and global competitors."
    name = "CompetitorAnalysisAgent"
    icon = "Search"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="competitor_name", display_name="Competitor Name"),
    ]

    outputs = [Output(display_name="Competitive Insights", name="output", method="analyze_competitor")]

    def analyze_competitor(self) -> Message:
        api_key = self.groq_api_key

        if not api_key:

            api_key = os.getenv("GROQ_API_KEY")

        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.3-70b-versatile")
        prompt = (f"Analyze competitor: {self.competitor_name}. "
                  "Identify their strengths, weaknesses, and how Harxit Tech can beat them with better AI solutions.")
        response = llm.invoke(prompt)
        return Message(text=response.content)
