import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class AutomationBuilderAgent(Component):
    display_name: str = "HT 18: Automation Builder Agent"
    description: str = "Maps internal automation steps for the timetable. NO PROPOSALS."
    name = "HarxitAutomationBuilderV2" # Unique name
    icon = "Zap"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="plan_data", display_name="Project Plan"),
    ]

    outputs = [Output(display_name="Automation Logic", name="output", method="build_logic")]

    def build_logic(self) -> Message:
        api_key = self.groq_api_key or os.getenv("GROQ_API_KEY")
        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.1-8b-instant")
        
        prompt = (f"Plan: {self.plan_data}\n\n"
                  "SYSTEM INSTRUCTION: DO NOT WRITE A PROPOSAL. "
                  "FOCUS ON TECHNICAL AUTOMATION. For the given 30-day plan, list 3 specific automation workflows (n8n/Python) "
                  "that Harxit Tech must build to hit the Week 2 and Week 3 deadlines on time.")
        
        response = llm.invoke(prompt)
        return Message(text=f"--- AUTOMATION STRATEGY ---\n\n{response.content}")
