import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class TrainingAgent(Component):
    display_name: str = "HT 29: Training Agent"
    description: str = "Generates sales scripts and training materials."
    name = "TrainingAgent"
    icon = "BookOpen"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="skill_topic", display_name="Skill/Topic"),
    ]

    outputs = [Output(display_name="Training Material", name="output", method="generate_training")]

    def generate_training(self) -> Message:
        api_key = self.groq_api_key

        if not api_key:

            api_key = os.getenv("GROQ_API_KEY")

        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.3-70b-versatile")
        prompt = (f"Harxit Tech needs to train interns on: {self.skill_topic}. "
                  "Provide a comprehensive sales script and a training checklist.")
        response = llm.invoke(prompt)
        return Message(text=response.content)
