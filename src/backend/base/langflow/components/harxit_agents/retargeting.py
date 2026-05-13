import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class RetargetingAgent(Component):
    display_name: str = "HT 13: Retargeting Agent"
    description: str = "Retargets interested but non-converted leads with new offers."
    name = "RetargetingAgent"
    icon = "RefreshCcw"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="old_lead_data", display_name="Old Lead Data"),
    ]

    outputs = [Output(display_name="Retargeting Offer", name="output", method="generate_retargeting")]

    def generate_retargeting(self) -> Message:
        api_key = self.groq_api_key

        if not api_key:

            api_key = os.getenv("GROQ_API_KEY")

        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.3-70b-versatile")
        prompt = (f"Lead Data: {self.old_lead_data}. "
                  "Create a special 'Limited Time' retargeting offer for this lead to bring them back into the sales funnel.")
        response = llm.invoke(prompt)
        return Message(text=response.content)
