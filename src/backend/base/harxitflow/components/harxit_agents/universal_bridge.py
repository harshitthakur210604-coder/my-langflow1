import os
import requests
import smtplib
from email.mime.text import MIMEText
from lfx.custom import Component
from lfx.io import MessageTextInput, Output, SecretStrInput, DropdownInput
from lfx.schema.message import Message
from pydantic.v1 import SecretStr

class HTUniversalBridge(Component):
    display_name: str = "HT Bridge: Unlimited Leads Hub (Free)"
    description: str = "Google Sheets ➔ Telegram Alerts ➔ WhatsApp Click-to-Chat ➔ Email."
    name = "HTUniversalBridge"
    icon = "Zap"

    inputs = [
        MessageTextInput(name="google_sheet_url", display_name="Google Sheet CSV Link"),
        SecretStrInput(name="telegram_bot_token", display_name="Telegram Bot Token", info="Create via @BotFather (100% Free)", required=False),
        MessageTextInput(name="telegram_chat_id", display_name="Telegram Chat ID", info="Get via @userinfobot", required=False),
        SecretStrInput(name="email_app_password", display_name="Gmail App Password", required=False),
        MessageTextInput(name="sender_email", display_name="Your Email", value="admin@harxittech.com"),
    ]
    
    outputs = [
        Output(display_name="Automation Report", name="output", method="process"),
    ]

    def send_telegram_alert(self, lead_name, lead_phone, lead_req):
        if not self.telegram_bot_token or not self.telegram_chat_id:
            return False
        
        # WhatsApp Click-to-Chat Link
        wa_link = f"https://wa.me/{lead_phone.replace('+', '').replace(' ', '')}?text=Hello%20{lead_name}!%20I%20am%20from%20Harxit%20Tech%20regarding%20your%20requirement:%20{lead_req}"
        
        text = (f"🚀 *New Lead Alert - Harxit Tech*\n\n"
                f"👤 *Name:* {lead_name}\n"
                f"📞 *Phone:* {lead_phone}\n"
                f"📝 *Requirement:* {lead_req}\n\n"
                f"👉 [Click to Chat on WhatsApp]({wa_link})")
        
        url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
        payload = {"chat_id": self.telegram_chat_id, "text": text, "parse_mode": "Markdown"}
        
        try:
            requests.post(url, json=payload)
            return True
        except Exception:
            return False

    def send_email(self, to_email, lead_name):
        if not self.email_app_password:
            return False
        msg = MIMEText(f"Hello {lead_name},\n\nWe have received your request. Our team will contact you shortly.\n\nBest Regards,\nHarxit Tech")
        msg['Subject'] = 'Harxit Tech - Lead Received'
        msg['From'] = self.sender_email
        msg['To'] = to_email

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.sender_email, self.email_app_password)
                server.send_message(msg)
            return True
        except Exception:
            return False

    def process(self) -> Message:
        # Mocking data from Google Sheets
        mock_leads = [
            {"name": "John Doe", "phone": "+919876543210", "email": "john@example.com", "req": "AI Automation"},
        ]
        
        report = []
        for lead in mock_leads:
            tg = "Sent" if self.send_telegram_alert(lead['name'], lead['phone'], lead['req']) else "Failed/Skipped"
            em = "Sent" if self.send_email(lead['email'], lead['name']) else "Skipped"
            
            wa_link = f"https://wa.me/{lead['phone'].replace('+', '').replace(' ', '')}"
            report.append(f"Lead: {lead['name']} | TG Alert: {tg} | Email: {em} | [WA Link]({wa_link})")

        return Message(text="--- HARXIT TECH FREE INTEGRATION REPORT ---\n\n" + "\n".join(report))
