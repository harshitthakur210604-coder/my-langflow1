import os
import requests
import sqlite3
import json
from fastapi import FastAPI, Request, HTTPException, Query
from langchain_groq import ChatGroq

app = FastAPI()

# --- Configuration (Set these in Render Environment Variables) ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")  # Meta Permanent Token
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN", "harxit_tech_secret")

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect('harxit_memory.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history
                 (sender_id TEXT PRIMARY KEY, history TEXT)''')
    conn.commit()
    return conn

def get_memory(sender_id):
    conn = init_db()
    c = conn.cursor()
    c.execute("SELECT history FROM chat_history WHERE sender_id=?", (sender_id,))
    result = c.fetchone()
    conn.close()
    if result:
        return json.loads(result[0])
    return []

def save_memory(sender_id, history):
    conn = init_db()
    c = conn.cursor()
    history = history[-10:]
    c.execute("INSERT OR REPLACE INTO chat_history (sender_id, history) VALUES (?, ?)",
              (sender_id, json.dumps(history)))
    conn.commit()
    conn.close()

# --- AI Logic ---
def get_ai_response(sender_id, message_text):
    if not GROQ_API_KEY:
        return "System Error: API Key missing."
    
    llm = ChatGroq(api_key=GROQ_API_KEY, model="llama-3.1-8b-instant")
    
    chat_history = get_memory(sender_id)
    history_str = "\n".join([f"{m['role']}: {m['content']}" for m in chat_history])
    
    context = "Harxit Tech is an AI Automation Agency specializing in Web Dev, SEO, CRM, and AI Agents."
    prompt = (f"SYSTEM: You are the AI Sales Assistant of Harxit Tech. Friendly, professional tone. "
              f"CONTEXT: {context}\n\n"
              f"PAST CONVERSATION:\n{history_str}\n\n"
              f"CUSTOMER SAYS: {message_text}\n\n"
              f"TASK: Reply naturally in Hindi/English (Hinglish). Suggest Harxit Tech services. "
              f"Keep it concise for WhatsApp/Telegram.")

    response = llm.invoke(prompt)
    ai_reply = response.content
    
    chat_history.append({"role": "user", "content": message_text})
    chat_history.append({"role": "assistant", "content": ai_reply})
    save_memory(sender_id, chat_history)
    
    return ai_reply

# --- Webhook Endpoints ---

@app.get("/")
def home():
    return {"status": "Harxit Tech AI Server (Meta API) is Online"}

# 1. Telegram Webhook
@app.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    data = await request.json()
    if "message" in data:
        chat_id = str(data["message"]["chat"]["id"])
        text = data["message"].get("text", "")
        if text:
            reply = get_ai_response(chat_id, text)
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            requests.post(url, json={"chat_id": chat_id, "text": reply})
    return {"status": "ok"}

# 2. WhatsApp Webhook (Meta Cloud API)
@app.get("/webhook/whatsapp")
def verify_whatsapp(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge")
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Verification failed")

@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    data = await request.json()
    try:
        if "messages" in data["entry"][0]["changes"][0]["value"]:
            message = data["entry"][0]["changes"][0]["value"]["messages"][0]
            phone_number = message["from"]
            text = message["text"]["body"]
            
            reply = get_ai_response(phone_number, text)
            
            url = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
            headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
            payload = {
                "messaging_product": "whatsapp",
                "to": phone_number,
                "type": "text",
                "text": {"body": reply}
            }
            requests.post(url, json=payload, headers=headers)
    except Exception:
        pass
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
