import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class QAAgent(Component):
    display_name: str = "HT 32: QA Agent"
    description: str = "Reviews final project output for quality and bugs."
    name = "QAAgent"
    icon = "CheckCircle"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="project_output", display_name="Final Project Content/URL"),
    ]

    outputs = [Output(display_name="QA Report", name="output", method="run_qa")]

    def run_qa(self) -> Message:
        api_key = self.groq_api_key or os.getenv("GROQ_API_KEY")
        # Forced model: llama-3.1-8b-instant
        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.1-8b-instant")
        
        prompt = (f"Project Content: {self.project_output}\n\n"
                  "Perform a rigorous Quality Assurance check. Identify potential bugs and UI/UX improvements. "
                  "Provide a Pass/Fail status and a list of fixes if needed.")
        
        response = llm.invoke(prompt)
        # Pass through the location if it exists in project_output
        loc_header = ""
        if "LOCATION:" in str(self.project_output):
            loc_header = str(self.project_output).split("\n\n")[0] + "\n\n"
            
        return Message(text=loc_header + response.content)
