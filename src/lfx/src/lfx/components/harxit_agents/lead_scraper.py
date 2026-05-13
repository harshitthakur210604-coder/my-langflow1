import os
from lfx.custom.custom_component.component import Component
from lfx.io import (
    MessageTextInput,
    Output,
    SecretStrInput,
    DropdownInput,
)
from lfx.schema.data import Data

class LeadScraperAgent(Component):
    display_name: str = "HT 1: Lead Scraper Agent"
    description: str = "Extracts business leads using ScrapeGraph (Paid) or DuckDuckGo (Free)."
    name = "LeadScraperAgent"
    icon = "Search"

    inputs = [
        DropdownInput(
            name="service",
            display_name="Scraping Service",
            options=["ScrapeGraph (API Key Required)", "DuckDuckGo (Free)"],
            value="DuckDuckGo (Free)",
            info="Choose 'DuckDuckGo' for free unlimited search or 'ScrapeGraph' for AI-powered scraping.",
        ),
        SecretStrInput(
            name="api_key",
            display_name="ScrapeGraph API Key",
            required=False,
            password=True,
            info="Only required if using ScrapeGraph service.",
        ),
        MessageTextInput(
            name="location",
            display_name="Location",
            info="Target city or area (e.g., Agra, Delhi).",
            value="Agra",
        ),
        MessageTextInput(
            name="business_type",
            display_name="Business Type",
            info="Type of business (e.g., School, Hospital, Gym).",
            value="Schools",
        ),
    ]

    outputs = [
        Output(display_name="Leads Data", name="leads", method="scrape_leads"),
    ]

    def scrape_leads(self) -> Data:
        search_query = f"{self.business_type} in {self.location} contact details phone email"
        
        if "DuckDuckGo" in self.service:
            try:
                from duckduckgo_search import DDGS
            except ImportError:
                raise ImportError("Please install duckduckgo-search: `pip install duckduckgo-search`")
            
            results = []
            with DDGS() as ddgs:
                ddgs_results = ddgs.text(search_query, max_results=10)
                for r in ddgs_results:
                    results.append({
                        "name": r.get("title"),
                        "link": r.get("href"),
                        "snippet": r.get("body"),
                        "source": "DuckDuckGo"
                    })
            return Data(data=results)

        else:
            # ScrapeGraph Logic
            try:
                from scrapegraph_py import Client
            except ImportError as e:
                raise ImportError("Please install scrapegraph-py: `pip install scrapegraph-py`") from e

            api_key = self.api_key or os.getenv("SCRAPEGRAPH_API_KEY")
            if not api_key:
                raise ValueError("ScrapeGraph API Key is required for this service.")
                
            sgai_client = Client(api_key=api_key)
            try:
                search_prompt = f"Find contact details (Business Name, Phone, Email, Website) for {self.business_type} in {self.location}. Return as JSON."
                response = sgai_client.searchscraper(user_prompt=search_prompt)
                sgai_client.close()
                return Data(data=response)
            except Exception:
                sgai_client.close()
                raise
