import os
import time
import requests
import speech_recognition as sr
from groq import Groq
from gtts import gTTS
import pygame

# --- CONFIGURATION ---
GROQ_API_KEY = "YOUR_GROQ_API_KEY" # Apni key yahan dalein
LANGFLOW_API_URL = "http://localhost:7860/api/v1/run/YOUR_FLOW_ID" # Langflow run URL
GROQ_CLIENT = Groq(api_key=GROQ_API_KEY)

def speak(text):
    """Text ko bol ke sunata hai (Hindi/English support)"""
    print(f"Agent: {text}")
    tts = gTTS(text=text, lang='hi') # 'hi' for Hindi, 'en' for English
    tts.save("response.mp3")
    
    pygame.mixer.init()
    pygame.mixer.music.load("response.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    pygame.mixer.quit()
    os.remove("response.mp3")

def listen():
    """Aapki voice sun ke text mein badalta hai (Using Groq Whisper)"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening... (Aap boliye)")
        audio = r.listen(source)
        
    try:
        # Save temporary audio file
        with open("temp_audio.wav", "wb") as f:
            f.write(audio.get_wav_data())
            
        # Transcribe using Groq Whisper (Free & Fast)
        with open("temp_audio.wav", "rb") as file:
            transcription = GROQ_CLIENT.audio.transcriptions.create(
                file=("temp_audio.wav", file.read()),
                model="whisper-large-v3",
                response_format="text",
                language="hi" # Hindi support
            )
        os.remove("temp_audio.wav")
        print(f"You said: {transcription}")
        return transcription
    except Exception as e:
        print(f"Error: {e}")
        return None

def call_langflow(message):
    """Langflow Flow ko call karta hai"""
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    try:
        response = requests.post(LANGFLOW_API_URL, json=payload)
        result = response.json()
        # Path might vary based on Langflow version, adjusting to common one
        return result['outputs'][0]['outputs'][0]['results']['message']['text']
    except Exception as e:
        return f"System error: {e}"

if __name__ == "__main__":
    speak("Namaste! Main aapka business growth agent hoon. Main aapke liye kya kaam karun?")
    
    while True:
        user_input = listen()
        if user_input:
            if "shukriya" in user_input.lower() or "bye" in user_input.lower():
                speak("Alvida! Aapka din shubh ho.")
                break
                
            speak("Samajh gaya, main check kar raha hoon...")
            
            # 1. Send to Langflow for processing (Instagram, Leads, Website data)
            response_text = call_langflow(user_input)
            
            # 2. Speak the response
            speak(response_text)
