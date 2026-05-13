import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class HarxitWorkingPlanAgent(Component):
    display_name: str = "HT 19: FINAL WORKING PLAN"
    description: str = "Generates the final 30-day technical execution plan. NO INVOICES."
    name = "HarxitWorkingPlanAgent"
    icon = "Terminal"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="tech_stack", display_name="Automation Logic"),
    ]

    outputs = [Output(display_name="Final Plan", name="output", method="generate_plan")]

    def generate_plan(self) -> Message:
        api_key = self.groq_api_key or os.getenv("GROQ_API_KEY")
        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.1-8b-instant")
        
        prompt = (f"Input Data: {self.tech_stack}\n\n"
                  "SYSTEM INSTRUCTION: DO NOT WRITE AN INVOICE. DO NOT WRITE A PROPOSAL. "
                  "YOU ARE THE CHIEF TECHNOLOGY OFFICER (CTO) OF HARXIT TECH. "
                  "GENERATE THE FINAL 30-DAY TECHNICAL EXECUTION TIMETABLE. "
                  "Include: 1. Tech Stack Details, 2. API Schema, 3. Folder Architecture, 4. Installation Commands. "
                  "All pricing must be in ₹ (INR) if mentioned, but focus on TECHNICAL TASKS.")
        
        response = llm.invoke(prompt)
        return Message(text=f"--- HARXIT TECH OFFICIAL 30-DAY WORKING PLAN ---\n\n{response.content}")
