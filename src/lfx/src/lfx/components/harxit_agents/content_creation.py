import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class ContentCreationAgent(Component):
    display_name: str = "HT 26: Content Creation Agent"
    description: str = "Generates Instagram posts, reels, and blogs."
    name = "ContentCreationAgent"
    icon = "PenTool"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="topic", display_name="Content Topic"),
    ]

    outputs = [Output(display_name="Marketing Content", name="output", method="generate_content")]

    def generate_content(self) -> Message:
        api_key = self.groq_api_key

        if not api_key:

            api_key = os.getenv("GROQ_API_KEY")

        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.3-70b-versatile")
        prompt = (f"Create a marketing plan for Harxit Tech on this topic: {self.topic}. "
                  "Include 1 Blog outline, 2 Instagram post ideas, and 1 Reel script.")
        response = llm.invoke(prompt)
        return Message(text=response.content)
