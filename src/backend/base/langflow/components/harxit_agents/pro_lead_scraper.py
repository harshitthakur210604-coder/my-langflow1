import http.client
import json
import os
import re
from lfx.custom.custom_component.component import Component
from lfx.io import (
    MessageTextInput, 
    Output, 
    SecretStrInput,
    IntInput,
    DropdownInput
)
from lfx.schema.message import Message

class ProLeadScraper(Component):
    display_name: str = "HT 1: Ultimate Pro Scraper (Google Maps + Search)"
    description: str = "Extracts 100% accurate LOCAL leads using Google Maps (Places) & Search."
    name = "ProLeadScraper"
    icon = "Search"

    inputs = [
        SecretStrInput(
            name="serper_api_key", 
            display_name="Serper API Key", 
            info="Get free key from serper.dev", 
            required=True,
            password=True
        ),
        MessageTextInput(
            name="location", 
            display_name="Location", 
            value="Agra",
            info="Target city or area (e.g., Agra, Delhi)."
        ),
        MessageTextInput(
            name="business_type", 
            display_name="Business Type / Niche", 
            info="Type of business (e.g., Schools, Gyms)."
        ),
        DropdownInput(
            name="country_code",
            display_name="Country",
            options=["in (India)", "us (USA)", "ae (UAE)", "gb (UK)"],
            value="in (India)",
            info="Set to 'in' for Indian leads to avoid international results."
        ),
        IntInput(
            name="num_results",
            display_name="Number of Leads",
            value=20,
            info="Max 100 per search."
        )
    ]

    outputs = [
        Output(display_name="Combined Leads Report", name="leads_text", method="scrape_google"),
        Output(display_name="Raw JSON Data", name="raw_json", method="get_raw_data")
    ]

    def _fetch_serper(self, endpoint: str, query: str, num: int, gl: str) -> dict:
        conn = http.client.HTTPSConnection("google.serper.dev")
        payload = json.dumps({"q": query, "num": num, "gl": gl})
        headers = {
            'X-API-KEY': self.serper_api_key,
            'Content-Type': 'application/json'
        }
        conn.request("POST", f"/{endpoint}", payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        return json.loads(data)

    def scrape_google(self) -> Message:
        if not self.business_type:
            return Message(text="Error: Business Type is empty.")
            
        gl = self.country_code.split(' ')[0]
        location = self.location
        niche = re.sub(r'^\d+[\.\)]\s*', '', self.business_type.split('\n')[0]).strip()
        
        query = f"{niche} in {location}"
        all_leads = []

        try:
            # 1. Fetch from PLACES (Google Maps) - High Accuracy for Local Business
            maps_data = self._fetch_serper("places", query, self.num_results, gl)
            for item in maps_data.get("places", []):
                lead_str = (
                    f"🏢 NAME: {item.get('title')}\n"
                    f"📞 PHONE: {item.get('phoneNumber', 'N/A')}\n"
                    f"🌐 WEBSITE: {item.get('website', 'N/A')}\n"
                    f"🏠 ADDRESS: {item.get('address', 'N/A')}\n"
                    f"⭐ RATING: {item.get('rating', 'N/A')} ({item.get('ratingCount', 0)} reviews)\n"
                )
                all_leads.append(lead_str)

            # 2. Fetch from SEARCH (Organic) - For extra depth if Maps has few results
            if len(all_leads) < 5:
                search_data = self._fetch_serper("search", f"{query} contact details", 10, gl)
                for item in search_data.get("organic", []):
                    # Skip common directory sites to keep it clean
                    if any(x in item.get('link', '') for x in ['justdial', 'indiamart', 'facebook', 'youtube', 'linkedin']):
                        continue
                    lead_str = (
                        f"🏢 NAME: {item.get('title')}\n"
                        f"🌐 LINK: {item.get('link')}\n"
                        f"📝 INFO: {item.get('snippet')}\n"
                    )
                    all_leads.append(lead_str)

        except Exception as e:
            return Message(text=f"Error fetching leads: {str(e)}")

        if not all_leads:
            return Message(text=f"No local leads found for '{niche}' in '{location}'. Try a broader niche.")

        report = f"🚀 HARXIT TECH ULTIMATE LEAD REPORT\n"
        report += f"📍 Location: {location} ({gl.upper()})\n"
        report += f"🔍 Targeted Niche: {niche}\n"
        report += f"✅ Total Qualified Leads: {len(all_leads)}\n"
        report += "="*35 + "\n\n"
        report += "\n---\n".join(all_leads)
        
        return Message(text=report)

    def get_raw_data(self) -> Message:
        return Message(text="Raw Data Output")
