import pyttsx3
import serial
import time
import re
import google.generativeai as genai
import dotenv
import os

arduino1 = serial.Serial('COM13', 960)  # Primary Arduino for chatbot control
arduino2 = serial.Serial('COM14', 960)  # Secondary Arduino for servo motor control
time.sleep(2)  # Wait for Arduino to initialize
# Set up TTS (Text-to-Speech) with male voice
engine = pyttsx3.init()
engine.setProperty("rate", 10)
voices = engine.getProperty("voices")
for voice in voices:
    if "male" in voice.name.lower():
        engine.setProperty("voice", voice.id)
        break
else:
    engine.setProperty("voice", voices[0].id)  # fallback to first voice if no "male" found

# Load environment variables
dotenv()

# Gemini API setup
GEMINI_API_KEY = "........."
genai.configure(api_key=GEMINI_API_KEY)

# Gemini model instance
model = genai.GenerativeModel("gemini-pro")

# Domain-specific context for Kedarnath
KEDARNATH_CONTEXT = """
You are a knowledgeable and polite Kedarnath travel guide. Only answer questions related to:
- Travel routes
- Stay options
- Helicopter and trek info
- Weather and safety
- Mythology, temples, history

Do not answer anything outside Kedarnath or religious travel. Keep responses short and helpful.
"""

# Get user voice input
def get_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Listening...")
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=8)
            text = r.recognize_google(audio)
            print("🗣️ You:", text)
            return text.lower()
        except:
            speak("Sorry, I couldn't understand.")
            return None

# Get Gemini-generated response based on Kedarnath context
def get_kedarnath_reply(question):
    prompt = KEDARNATH_CONTEXT + f"\n\nUser: {question}\nGuide:"
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "I'm facing trouble connecting to the internet or processing your question."

# Main loop
def main():
    speak("Namaste! I am ASTRA, your online Kedarnath guide.")
    stop_words = {"stop", "exit", "bye", "quit"}

    while True:
        user_input = get_voice_input()
        if user_input:
            if any(word in user_input for word in stop_words):
                speak("Goodbye! Har Har Mahadev!")
                break
            answer = get_kedarnath_reply(user_input)
            speak(answer)

# Entry point
if __name__ == "__main__":
    main()