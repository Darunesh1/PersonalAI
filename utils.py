import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config
from conv import EMAIL, IP_URL, NEWS, NEWS_URL, PASSWORD, SMTP_PORT, SMTP_URL, WEATHER, WEATHER_URL
import gtts
from pydub import AudioSegment
from pydub.playback import play
import os



def speak(text):
    tts = gtts.gTTS(text=text, lang='en')
    tts.save("audio.wav")
    
    audio = AudioSegment.from_mp3("audio.wav")
    os.remove("audio.wav")
    audio=audio.speedup(playback_speed=1.5)
    
    play(audio)


def find_my_ip():
    ip_address = requests.get(IP_URL).json()
    return ip_address["ip"]

def search_on_wikipedia(query):
    try:
        results = wikipedia.summary(query, sentences=2)
        return results
    except wikipedia.exceptions.DisambiguationError as e:
        return str(e.options)
    
def search_on_google(query):
    kit.search(query)
    
def youtube(video):
    kit.playonyt(video)
    
def send_email(receiver, subject, message):
    if EMAIL=="" or PASSWORD=="":
        return False
    try:
        email=EmailMessage()
        email['To']=receiver
        email['Subject']=subject
        email['From']=EMAIL
        
        email.set_content(message)
        server=smtplib.SMTP(SMTP_URL,SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(email)
        server.close()
        return True
    except Exception as e:
        print(e)
        return False
    
def get_news():
    news_headlines = []
    url = NEWS_URL
    try:
        result = requests.get(
            url,
            params={
                "apiKey": NEWS,
                "q": "business",
                "country": "in",
                "category": "technology"
            }
        ).json() 
        articles = result["results"]
        for article in articles:
            news_headlines.append(article["title"])
        return news_headlines[:4]
    except Exception as e:
        print(e)
        return news_headlines


def weather_forecast(city):
    url = WEATHER_URL
    try:
        result = requests.get(
            url,
            params={
                "appid": WEATHER,
                "q": city,
            }
        ).json()
        weather = result["weather"][0]["main"]
        temperature = result["main"]["temp"]
        feels_like = result["main"]["feels_like"]
        return weather, f"{temperature}°C", f"{feels_like}°C"
    except Exception as e:
        print(e)
        return None, None, None
