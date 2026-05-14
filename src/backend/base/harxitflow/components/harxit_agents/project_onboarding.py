import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput, DropdownInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class ProjectOnboardingAgent(Component):
    display_name: str = "HT 31: Project Onboarding Agent"
    description: str = "Handles new client data and sets up the project workflow."
    name = "ProjectOnboardingAgent"
    icon = "UserPlus"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="client_details", display_name="Client Name & Service"),
        MessageTextInput(name="project_scope", display_name="Project Scope"),
        DropdownInput(
            name="client_location", 
            display_name="Client Location", 
            options=["India", "International"], 
            value="India"
        ),
    ]

    outputs = [Output(display_name="Onboarding Report", name="output", method="onboard_client")]

    def onboard_client(self) -> Message:
        api_key = self.groq_api_key or os.getenv("GROQ_API_KEY")
        # Forced model: llama-3.1-8b-instant
        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.1-8b-instant")
        
        prompt = (f"Client: {self.client_details}\nScope: {self.project_scope}\nLocation: {self.client_location}\n\n"
                  "Generate a professional project onboarding report. List the first 5 technical steps Harxit Tech needs to take. "
                  "IMPORTANT: Mention the location in the report.")
        
        response = llm.invoke(prompt)
        # We append location to the text so the next agent can see it
        result_text = f"LOCATION: {self.client_location}\n\n" + response.content
        return Message(text=result_text)
