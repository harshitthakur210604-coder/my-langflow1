import os
from lfx.custom.custom_component.component import Component
from lfx.io import (
    MessageTextInput,
    Output,
    HandleInput,
)
from lfx.schema.data import Data
from lfx.schema.message import Message
import requests

class N8nSenderComponent(Component):
    display_name: str = "HT: n8n Outreach Bridge"
    description: str = "Sends lead data to n8n for automated WhatsApp or Email sequences."
    name = "N8nSender"
    icon = "Send"

    inputs = [
        MessageTextInput(
            name="webhook_url",
            display_name="n8n Webhook URL",
            required=True,
            info="The URL of your n8n webhook (must start with http:// or https://).",
        ),
        HandleInput(
            name="payload",
            display_name="Data Payload",
            info="Connect the Lead Scorer or Extractor here.",
            input_types=["Message", "Data", "dict", "str"],
        ),
    ]

    outputs = [
        Output(display_name="n8n Response", name="response", method="send_to_n8n"),
    ]

    def send_to_n8n(self) -> Data:
        # Check if webhook_url is actually a URL and not the lead data
        if not self.webhook_url or not str(self.webhook_url).startswith(("http://", "https://")):
            return Data(data={
                "error": "Invalid Webhook URL. Please ensure the 'n8n Webhook URL' field contains a valid URL and not the lead data. Check your wiring!"
            })

        # Process payload
        data_to_send = {}
        if isinstance(self.payload, Message):
            data_to_send = {"text": self.payload.text}
        elif isinstance(self.payload, Data):
            data_to_send = self.payload.data
        elif isinstance(self.payload, dict):
            data_to_send = self.payload
        elif isinstance(self.payload, str):
            data_to_send = {"text": self.payload}
        else:
            data_to_send = {"data": str(self.payload)}

        try:
            response = requests.post(self.webhook_url, json=data_to_send, timeout=10)
            response.raise_for_status()
            
            # Try to return JSON if possible, else raw text
            try:
                return Data(data=response.json())
            except:
                return Data(data={"response_text": response.text})
                
        except Exception as e:
            return Data(data={"error": f"Failed to send to n8n: {str(e)}"})
