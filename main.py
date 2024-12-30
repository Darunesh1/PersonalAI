import pyttsx3
from datetime import datetime
from decouple import config
from conv import random_text, farewell_text
import speech_recognition as sr
from random import choice

engine = pyttsx3.init("sapi5")

engine.setProperty('volume', 2)
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

USER = config('USER')
HOSTNAME = config('BOT')

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def gree_me():
    hour = datetime.now().hour
    if 6 <= hour < 12:
        speak(f"Good Morning {USER}")
    elif 12 <= hour < 18:
        speak(f"Good Afternoon {USER}")
    elif 18 <= hour < 20:
        speak(f"Good Evening {USER}")
    elif 20 <= hour or hour < 6:
        speak(f"{USER}, you're not sleeping, are you?")
    speak(f"I am {HOSTNAME}, your assistant. How may I help you?")

def farewell():
    speak(choice(farewell_text))
    speak(f"This is {HOSTNAME} signing off")
    exit()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source)
            print("Recognizing...")
            task = r.recognize_google(audio, language='en-in')
            print(f"User said: {task}\n")
            return task
        except Exception as e:
            print("Error:", e)
            speak("I didn't catch that. Could you repeat?")
            return ""  # Return empty string instead of None or set

# Main logic
gree_me()

while True:
    task = take_command()
    if task:  # Ensure task is not empty
        task = task.lower()
        if "how are you" in task:
            speak("I am doing great, thank you for asking.")
        elif "stop" in task or "exit" in task:
            farewell()
        else:
            speak(choice(random_text))
