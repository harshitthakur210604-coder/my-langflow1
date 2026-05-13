import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class ClientSuccessAgent(Component):
    display_name: str = "HT 34: Client Success Agent"
    description: str = "Collects success data and creates case studies for new builds."
    name = "ClientSuccessAgent"
    icon = "Trophy"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="success_data", display_name="Project Achievements (e.g. 2x leads, 50% growth)"),
    ]

    outputs = [Output(display_name="Success Story", name="output", method="generate_case_study")]

    def generate_case_study(self) -> Message:
        api_key = self.groq_api_key or os.getenv("GROQ_API_KEY")
        # Forced model: llama-3.1-8b-instant
        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.1-8b-instant")
        
        prompt = (f"Success Data: {self.success_data}\n\n"
                  "Transform this data into a powerful 'Successful Build' case study. "
                  "Provide a professional write-up.")
        
        response = llm.invoke(prompt)
        # Pass through the location if it exists
        loc_header = ""
        if "LOCATION:" in str(self.success_data):
            loc_header = str(self.success_data).split("\n\n")[0] + "\n\n"
            
        return Message(text=loc_header + response.content)
