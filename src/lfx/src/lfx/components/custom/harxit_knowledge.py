from lfx.custom import Component
from lfx.io import MessageTextInput, Output
from lfx.schema import Data
import requests
from bs4 import BeautifulSoup

class HarxitTechKnowledge(Component):
    display_name = "HARXIT TECH Knowledge Base"
    description = "Reads company info from website or manual text"
    
    inputs = [
        MessageTextInput(name="url", display_name="Company Website URL", value="https://harxittech.com"), # Example
        MessageTextInput(name="manual_info", display_name="Manual Info (Optional)", 
                         info="Agar website nahi hai toh yahan company ki details likhein.",
                         value="HARXIT TECH: Best software solutions, Web/App Development, AI Automation."),
    ]
    
    outputs = [
        Output(name="company_context", display_name="Company Context", method="get_context"),
    ]

    def get_context(self) -> Message:
        context = f"Company Name: HARXIT TECH\n"
        if self.url and self.url.startswith("http"):
            try:
                response = requests.get(self.url, timeout=5)
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text()[:2000] # Limit to 2000 chars for efficiency
                context += f"Website Data: {text}\n"
            except:
                context += "Website not reachable, using manual info.\n"
        
        context += f"Services/Details: {self.manual_info}"
        return Message(text=context)
