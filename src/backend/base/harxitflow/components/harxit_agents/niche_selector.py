import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class HTNicheSelector(Component):
    display_name: str = "HT: Niche Selector"
    description: str = "Extracts the main business niche from a long analysis paragraph."
    name = "HTNicheSelector"
    icon = "Filter"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="raw_analysis", display_name="Raw Analysis from Niche Finder"),
    ]

    outputs = [
        Output(display_name="Clean Niche Keyword", name="clean_niche", method="process_niche"),
    ]

    def process_niche(self) -> Message:
        api_key = self.groq_api_key or os.getenv("GROQ_API_KEY")
        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.1-8b-instant")
        
        prompt = (f"Read this business analysis: '{self.raw_analysis}'\n\n"
                  "TASK: Identify the TOP 1 business niche or category mentioned (e.g., 'Schools', 'Gyms', 'Hospitals'). "
                  "Return ONLY the single word or short phrase. No explanation, no numbering.")
        
        response = llm.invoke(prompt)
        clean_text = response.content.strip().replace('"', '').replace('.', '')
        
        return Message(text=clean_text)
