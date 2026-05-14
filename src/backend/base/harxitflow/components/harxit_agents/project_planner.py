import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class ProjectPlannerAgent(Component):
    display_name: str = "HT 17: Project Planner Agent"
    description: str = "Generates a strict 30-day execution timetable. NO PROPOSALS."
    name = "HarxitProjectPlannerV2" # Unique name
    icon = "Calendar"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="project_details", display_name="Project Details"),
    ]

    outputs = [Output(display_name="Execution Plan", name="output", method="generate_plan")]

    def generate_plan(self) -> Message:
        api_key = self.groq_api_key or os.getenv("GROQ_API_KEY")
        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.1-8b-instant")
        
        prompt = (f"Project: {self.project_details}\n\n"
                  "SYSTEM INSTRUCTION: DO NOT WRITE A PROPOSAL. DO NOT USE THE WORD 'PROPOSAL'. "
                  "ACT AS A PROJECT MANAGER. GENERATE A STRICT 30-DAY WORKING TIMETABLE. "
                  "FORMAT:\n"
                  "Week 1 (Day 1-7): [Specific Tasks]\n"
                  "Week 2 (Day 8-14): [Specific Tasks]\n"
                  "Week 3 (Day 15-21): [Specific Tasks]\n"
                  "Week 4 (Day 22-30): [Specific Tasks]\n\n"
                  "Be extremely detailed with daily tasks for Harxit Tech developers.")
        
        response = llm.invoke(prompt)
        return Message(text=response.content)
