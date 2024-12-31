import os
from kivy.config import Config

width,height = 1920,1080

Config.set('graphics', 'width', width)
Config.set('graphics', 'height', height)
Config.set('graphics', 'fullscreen', 'True')

HOSTNAME=os.environ.get("BOT")
USER=os.environ.get("USER")

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

NEWS = os.environ.get("NEWS")
WEATHER = os.environ.get("WEATHER")
APP_ID = os.environ.get("APP_ID")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

IP_URL='https://api.ipify.org?format=json'

NEWS_URL="https://newsdata.io/api/1/latest"

WEATHER_URL="https://api.openweathermap.org/data/2.5/weather"

SMTP_URL="smtp.gmail.com"
SMTP_PORT=587

SCREEN_WIDTH = Config.getint('graphics', 'width')
SCREEN_HEIGHT = Config.getint('graphics', 'height')


farewell_text=[
    "Goodbye! Take care and see you soon.",
"Farewell! Stay safe and have a great day ahead.",
"Signing off now. Until next time!",
"It’s been a pleasure. Bye for now!",
"See you later! Don’t forget to smile.",
"Bye-bye! Catch you on the flip side.",
"Take care! I'm always here when you need me.",
"Adios! Stay awesome.",
"Goodnight, if it's bedtime! Talk to you soon.",
"Peace out! Have a wonderful time ahead.",
"So long! Looking forward to our next chat.",
"Stay safe and sound! Goodbye for now.",
"Ciao! I’ll be waiting for your return.",
"Keep shining! Goodbye for now.",
"That’s it from me. Take care, and bye-bye!",
"See you soon! Don’t hesitate to call me again.",
"Bye now! Remember, I’ve always got your back.",
"Later, alligator! Stay cool.",
"Catch you later! Wishing you the best.",
"Goodbye, my friend. Until we meet again.",
]

random_responses = [
        "I'm doing well, how about you?",
        "I'm here to assist you!",
        "Let's get started with your request."
    ]

