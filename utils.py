
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




# Function to find your IP address
def find_my_ip():
    try:
        ip_address = requests.get(IP_URL).json()
        return ip_address["ip"]
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to search on Wikipedia
def search_on_wikipedia(query):
    try:
        results = wikipedia.summary(query, sentences=2)
        return results
    except wikipedia.exceptions.DisambiguationError as e:
        return str(e.options)
    
# Function to search on Google
def search_on_google(query):
    kit.search(query)
    
# Function to play a YouTube video
def youtube(video):
    kit.playonyt(video)
    
# Function to send an email
def send_email(receiver, subject, message):
    if not EMAIL or not PASSWORD:
        return False
    try:
        email = EmailMessage()
        email['To'] = receiver
        email['Subject'] = subject
        email['From'] = EMAIL
        email.set_content(message)
        
        with smtplib.SMTP(SMTP_URL, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(email)
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    
# Function to get news headlines
def get_news():
    news_headlines = []
    try:
        result = requests.get(
            NEWS_URL,
            params={
                "apiKey": NEWS,
                "q": "business",
                "country": "in",
                "category": "technology"
            }
        ).json() 
        articles = result.get("results", [])
        for article in articles:
            news_headlines.append(article["title"])
        return news_headlines[:4]
    except Exception as e:
        print(f"Error: {e}")
        return news_headlines

# Function to get weather forecast for a city
def weather_forecast(city):
    try:
        result = requests.get(
            WEATHER_URL,
            params={
                "appid": WEATHER,
                "q": city,
            }
        ).json()
        
        weather = result.get("weather", [{}])[0].get("main")
        temperature = result.get("main", {}).get("temp")
        feels_like = result.get("main", {}).get("feels_like")
        
        if weather and temperature is not None and feels_like is not None:
            return weather, f"{temperature}°C", f"{feels_like}°C"
        return None, None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None
