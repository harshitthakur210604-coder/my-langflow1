import os
from lfx.custom.custom_component.component import Component
from lfx.io import (
    MessageTextInput,
    Output,
    SecretStrInput,
    DropdownInput,
)
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class NicheFinderAgent(Component):
    display_name: str = "HT 2: Niche Finder Agent"
    description: str = "Identifies high-demand business niches using Groq AI."
    name = "NicheFinderAgent"
    icon = "Target"

    inputs = [
        SecretStrInput(
            name="groq_api_key",
            display_name="Groq API Key",
            required=True,
        ),
        DropdownInput(
            name="model_name",
            display_name="Model",
            options=["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
            value="llama-3.3-70b-versatile",
        ),
        MessageTextInput(
            name="market_context",
            display_name="Market Context",
            info="Current market or general focus (e.g., Uttar Pradesh, Small Businesses).",
            value="General Indian Market",
        ),
    ]

    outputs = [
        Output(display_name="Niche Suggestions", name="niche_output", method="find_niche"),
    ]

    def find_niche(self) -> Message:
        api_key = self.groq_api_key

        if not api_key:

            api_key = os.getenv("GROQ_API_KEY")

        llm = ChatGroq(
            api_key=SecretStr(api_key).get_secret_value(),
            model=self.model_name,
        )
        
        prompt = (
            "As a business growth expert for Harxit Tech, targeting Small to Big Businesses in All India and International markets, "
            f"analyze the {self.market_context} market. "
            "Identify 5 high-demand business niches that need digital transformation (Websites, SEO, CRM, Apps). "
            "For each niche, explain WHY it is hot right now and what service Harxit Tech should pitch. "
            "Provide the response in a structured list format."
        )
        
        response = llm.invoke(prompt)
        return Message(text=response.content)
