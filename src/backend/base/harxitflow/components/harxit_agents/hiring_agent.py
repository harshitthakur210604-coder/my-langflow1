import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class HiringAgent(Component):
    display_name: str = "HT 28: Hiring Agent"
    description: str = "Helps in intern hiring and JD generation."
    name = "HiringAgent"
    icon = "UserPlus"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="role_name", display_name="Role Name"),
    ]

    outputs = [Output(display_name="Job Description", name="output", method="generate_jd")]

    def generate_jd(self) -> Message:
        api_key = self.groq_api_key

        if not api_key:

            api_key = os.getenv("GROQ_API_KEY")

        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.3-70b-versatile")
        prompt = (f"Role: {self.role_name} at Harxit Tech. "
                  "Generate a high-quality Job Description (JD) for an intern role, including responsibilities, requirements, and perks.")
        response = llm.invoke(prompt)
        return Message(text=response.content)
