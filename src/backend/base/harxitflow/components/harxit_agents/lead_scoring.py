import os
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class LeadScoringAgent(Component):
    display_name: str = "HT 4: Smart Lead Scoring Agent"
    description: str = "De-duplicates and categorizes leads with Phone and Email Extraction."
    name = "SmartLeadScoringAgent"
    icon = "Activity"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="lead_data", display_name="Lead Data", info="Data from Scraper to be scored and filtered."),
    ]

    outputs = [
        Output(display_name="Final Report Table", name="output", method="score_lead"),
        Output(display_name="Phone List", name="phone_list", method="extract_phones"),
        Output(display_name="Email List", name="email_list", method="extract_emails"),
        Output(display_name="Combined Contacts", name="combined_contacts", method="extract_all_contacts"),
    ]

    def score_lead(self) -> Message:
        api_key = self.groq_api_key or os.getenv("GROQ_API_KEY")
        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.3-70b-versatile")
        
        prompt = (f"Analyze this lead data: {self.lead_data}. \n\n"
                  "1. DE-DUPLICATE: Merge multiple entries of the same business.\n"
                  "2. CATEGORIZE: HOT (No website), WARM (Old website), COLD (Great presence).\n"
                  "3. EXTRACT: Find all Phone Numbers AND Emails.\n\n"
                  "OUTPUT FORMAT: Table with: Business Name | Category | Phone | Email | Reasoning.")
        
        response = llm.invoke(prompt)
        return Message(text=response.content)

    def extract_phones(self) -> Message:
        api_key = self.groq_api_key or os.getenv("GROQ_API_KEY")
        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.1-8b-instant")
        prompt = f"Extract ONLY Business Name and Phone Numbers from: {self.lead_data}. Format: Name - Phone"
        response = llm.invoke(prompt)
        return Message(text=response.content)

    def extract_emails(self) -> Message:
        api_key = self.groq_api_key or os.getenv("GROQ_API_KEY")
        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.1-8b-instant")
        prompt = f"Extract ONLY Business Name and Email Addresses from: {self.lead_data}. Format: Name - Email"
        response = llm.invoke(prompt)
        return Message(text=response.content)

    def extract_all_contacts(self) -> Message:
        api_key = self.groq_api_key or os.getenv("GROQ_API_KEY")
        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.1-8b-instant")
        prompt = f"Extract Business Name, Phone, and Email from: {self.lead_data}. Format: Name | Phone | Email"
        response = llm.invoke(prompt)
        return Message(text=response.content)
