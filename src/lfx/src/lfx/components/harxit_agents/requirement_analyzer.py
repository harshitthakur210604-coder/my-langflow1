import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class RequirementAnalyzerAgent(Component):
    display_name: str = "HT 5: Requirement Analyzer Agent"
    description: str = "Analyzes client needs and suggests the best services."
    name = "RequirementAnalyzerAgent"
    icon = "Search"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="client_query", display_name="Client Query", info="What the client said they need."),
    ]

    outputs = [Output(display_name="Service Suggestion", name="output", method="analyze_needs")]

    def analyze_needs(self) -> Message:
        api_key = self.groq_api_key

        if not api_key:

            api_key = os.getenv("GROQ_API_KEY")

        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.3-70b-versatile")
        prompt = (f"The client says: '{self.client_query}'. "
                  "Analyze their need. If they ask for a website, suggest adding a CRM and SEO. "
                  "If they ask for an app, suggest cloud hosting and maintenance. "
                  "Suggest a complete 'Digital Growth Package' from Harxit Tech.")
        response = llm.invoke(prompt)
        return Message(text=response.content)
