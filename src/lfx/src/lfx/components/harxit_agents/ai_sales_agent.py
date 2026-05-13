import os
import requests
import sqlite3
import json
from lfx.custom import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.message import Message
from langchain_groq import ChatGroq
from pydantic.v1 import SecretStr

class HTAISalesAgent(Component):
    display_name: str = "HT 41: AI Conversational Sales Agent (with Memory)"
    description: str = "Advanced Sales Agent for Cloud Deployment. Remembers customers and handles TG/WA."
    name = "HTAISalesAgent"
    icon = "Brain"

    inputs = [
        SecretStrInput(name="groq_api_key", display_name="Groq API Key", required=True),
        MessageTextInput(name="customer_message", display_name="Incoming Message"),
        MessageTextInput(name="sender_id", display_name="Sender ID (Phone/TG ID)", info="Used to identify the user for memory."),
        MessageTextInput(name="context", display_name="Company Context", value="Harxit Tech is an AI Automation Agency specializing in Web Dev, SEO, CRM, and AI Agents."),
        SecretStrInput(name="telegram_bot_token", display_name="Telegram Bot Token", required=False),
    ]
    
    outputs = [
        Output(display_name="AI Response", name="output", method="process"),
    ]

    def init_db(self):
        conn = sqlite3.connect('harxit_memory.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS chat_history 
                     (sender_id TEXT PRIMARY KEY, history TEXT)''')
        conn.commit()
        return conn

    def get_memory(self, sender_id):
        conn = self.init_db()
        c = conn.cursor()
        c.execute("SELECT history FROM chat_history WHERE sender_id=?", (sender_id,))
        result = c.fetchone()
        conn.close()
        if result:
            return json.loads(result[0])
        return []

    def save_memory(self, sender_id, history):
        conn = self.init_db()
        c = conn.cursor()
        # Keep only last 10 messages for context efficiency
        history = history[-10:]
        c.execute("INSERT OR REPLACE INTO chat_history (sender_id, history) VALUES (?, ?)", 
                  (sender_id, json.dumps(history)))
        conn.commit()
        conn.close()

    def process(self) -> Message:
        api_key = self.groq_api_key or os.getenv("GROQ_API_KEY")
        llm = ChatGroq(api_key=SecretStr(api_key).get_secret_value(), model="llama-3.1-8b-instant")
        
        # 1. Fetch Past History
        chat_history = self.get_memory(self.sender_id)
        history_str = "\n".join([f"{m['role']}: {m['content']}" for m in chat_history])

        # 2. Build Intelligent Prompt
        prompt = (f"SYSTEM: You are the AI Sales Assistant of Harxit Tech. Friendly, professional tone. "
                  f"CONTEXT: {self.context}\n\n"
                  f"PAST CONVERSATION:\n{history_str}\n\n"
                  f"CUSTOMER SAYS: {self.customer_message}\n\n"
                  f"TASK: Reply naturally. Remember what was discussed before. Suggest Harxit Tech services. "
                  f"Try to close the deal or get contact info.")
        
        response = llm.invoke(prompt)
        ai_reply = response.content

        # 3. Update Memory
        chat_history.append({"role": "user", "content": self.customer_message})
        chat_history.append({"role": "assistant", "content": ai_reply})
        self.save_memory(self.sender_id, chat_history)

        # 4. Telegram Auto-Reply (If deployed)
        if self.telegram_bot_token and self.sender_id.isdigit():
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            requests.post(url, json={"chat_id": self.sender_id, "text": ai_reply})

        return Message(text=ai_reply)
