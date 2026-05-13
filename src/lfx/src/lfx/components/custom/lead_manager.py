from lfx.custom import Component
from lfx.io import MessageTextInput, Output, DataInput
from lfx.schema import Data
import sqlite3
import datetime

class LeadManager(Component):
    display_name = "Bharat Lead Manager"
    description = "Saves and retrieves leads from a local database (Zero Cost)"
    
    inputs = [
        MessageTextInput(name="lead_name", display_name="Lead Name", value=""),
        MessageTextInput(name="lead_contact", display_name="Contact (Insta/WA/Email)", value=""),
        MessageTextInput(name="lead_query", display_name="Query/Interests", value=""),
        MessageTextInput(name="action", display_name="Action (save/report)", value="save"),
    ]
    
    outputs = [
        Output(name="status", display_name="Status/Report", method="process_leads"),
    ]

    def process_leads(self) -> Message:
        conn = sqlite3.connect("business_leads.db")
        cursor = conn.cursor()
        
        # Table banayein agar nahi hai
        cursor.execute('''CREATE TABLE IF NOT EXISTS leads 
                         (id INTEGER PRIMARY KEY, name TEXT, contact TEXT, query TEXT, date TEXT)''')
        
        if self.action == "save" and self.lead_name:
            date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO leads (name, contact, query, date) VALUES (?, ?, ?, ?)",
                           (self.lead_name, self.lead_contact, self.lead_query, date_str))
            conn.commit()
            result = f"Done! Lead '{self.lead_name}' save ho gayi hai."
        else:
            # Report mode: Aaj ki leads dikhao
            cursor.execute("SELECT name, query FROM leads WHERE date >= date('now', 'start of day')")
            today_leads = cursor.fetchall()
            if not today_leads:
                result = "Aaj koi nayi lead nahi aayi hai."
            else:
                leads_text = ", ".join([f"{l[0]} ({l[1]})" for l in today_leads])
                result = f"Aaj ki leads ye hain: {leads_text}"
        
        conn.close()
        return Message(text=result)
