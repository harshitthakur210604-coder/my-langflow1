import os
import sqlite3
import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from langchain_groq import ChatGroq
from datetime import datetime

app = FastAPI()

# --- Configuration ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect('harxit_memory.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history
                 (sender_id TEXT PRIMARY KEY, history TEXT, last_updated DATETIME)''')
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
    history = history[-20:]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT OR REPLACE INTO chat_history (sender_id, history, last_updated) VALUES (?, ?, ?)",
              (sender_id, json.dumps(history), now))
    conn.commit()
    conn.close()

# --- AI Logic (Handles memory and thinking) ---
def get_ai_response(sender_id, message_text):
    if not GROQ_API_KEY:
        return "Error: Groq API Key missing."
    
    llm = ChatGroq(api_key=GROQ_API_KEY, model="llama-3.1-8b-instant")
    chat_history = get_memory(sender_id)
    history_str = "\n".join([f"{m['role']}: {m['content']}" for m in chat_history])
    
    context = "Harxit Tech is an AI Automation Agency. We build AI Agents and CRM solutions."
    prompt = f"SYSTEM: {context}\n\nPAST:\n{history_str}\n\nUSER: {message_text}\n\nREPLY (Hinglish):"
    
    response = llm.invoke(prompt)
    ai_reply = response.content
    
    chat_history.append({"role": "user", "content": message_text, "time": datetime.now().strftime("%H:%M")})
    chat_history.append({"role": "assistant", "content": ai_reply, "time": datetime.now().strftime("%H:%M")})
    save_memory(sender_id, chat_history)
    
    return ai_reply

# --- Webhook (For receiving data from Telegram or manual entry) ---
@app.post("/webhook/incoming")
async def incoming_data(request: Request):
    data = await request.json()
    sender = data.get("sender", "Unknown")
    message = data.get("message", "")
    if message:
        get_ai_response(sender, message)
    return {"status": "processed"}

@app.get("/")
def home():
    return {"status": "Harxit Hybrid CRM Online", "dashboard": "/dashboard"}

# --- HARXIT HYBRID CRM DASHBOARD ---
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    conn = init_db()
    c = conn.cursor()
    c.execute("SELECT sender_id, last_updated FROM chat_history ORDER BY last_updated DESC")
    contacts = c.fetchall()
    conn.close()

    contact_list_html = "".join([f"""
        <div class="contact" onclick="loadChat('{c[0]}')">
            <div class="name">{c[0]}</div>
            <div class="time">{c[1]}</div>
        </div>
    """ for c in contacts])

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Harxit Tech | Hybrid CRM</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; display: flex; height: 100vh; background: #f0f2f5; }}
            #sidebar {{ width: 300px; background: white; border-right: 1px solid #ddd; overflow-y: auto; }}
            #chat-area {{ flex: 1; display: flex; flex-direction: column; background: #e5ddd5; }}
            .header {{ background: #075e54; color: white; padding: 15px; font-weight: bold; display: flex; justify-content: space-between; align-items: center; }}
            .contact {{ padding: 15px; border-bottom: 1px solid #eee; cursor: pointer; transition: 0.3s; }}
            .contact:hover {{ background: #f5f5f5; }}
            #messages {{ flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; }}
            .msg {{ max-width: 70%; padding: 10px; border-radius: 10px; margin-bottom: 10px; }}
            .user {{ align-self: flex-end; background: #dcf8c6; }}
            .bot {{ align-self: flex-start; background: white; }}
            .wa-btn {{ background: #25d366; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; text-decoration: none; font-size: 14px; }}
            @media (max-width: 600px) {{ body {{ flex-direction: column; }} #sidebar {{ width: 100%; height: 40%; }} }}
        </style>
    </head>
    <body>
        <div id="sidebar">
            <div class="header">Harxit CRM</div>
            <div id="contact-list">{contact_list_html}</div>
        </div>
        <div id="chat-area">
            <div class="header">
                <span id="chat-header">Select a contact</span>
                <a id="wa-link" href="#" target="_blank" class="wa-btn" style="display:none;">Open in WhatsApp</a>
            </div>
            <div id="messages"></div>
        </div>

        <script>
            async function loadChat(senderId) {{
                document.getElementById('chat-header').innerText = "Chat with " + senderId;
                const waLink = document.getElementById('wa-link');
                
                // If it's a phone number, create direct WhatsApp Web link
                if(senderId.match(/^\d+$/) || senderId.includes('+')) {{
                    const cleanNum = senderId.replace(/\D/g, '');
                    waLink.href = `https://web.whatsapp.com/send?phone=${{cleanNum}}`;
                    waLink.style.display = 'block';
                }} else {{
                    waLink.style.display = 'none';
                }}

                const response = await fetch('/api/chat/' + senderId);
                const history = await response.json();
                document.getElementById('messages').innerHTML = history.map(msg => 
                    `<div class="msg ${{msg.role === 'user' ? 'user' : 'bot'}}">
                        ${{msg.content}}
                        <div style="font-size:10px; color:#888; text-align:right;">${{msg.time || ''}}</div>
                    </div>`
                ).join('');
                const div = document.getElementById('messages');
                div.scrollTop = div.scrollHeight;
            }}
        </script>
    </body>
    </html>
    """

@app.get("/api/chat/{sender_id}")
async def get_chat_api(sender_id: str):
    return get_memory(sender_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
