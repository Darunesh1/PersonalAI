import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config

EMAIL=""
PASSWORD=""
NEWS=config("NEWS")
WEATHER=config("WEATHER")


def find_my_ip():
    ip_address = requests.get('https://api.ipify.org?format=json').json()
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
        server=smtplib.SMTP('smtp.gmail.com',587)
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
    url = f"https://newsdata.io/api/1/latest?apikey={NEWS}&q=business&country=in&category=technology"
    try:
        result = requests.get(url).json() 
        articles = result["results"]
        for article in articles:
            news_headlines.append(article["title"])
        return news_headlines[:4]
    except Exception as e:
        print(e)
        return news_headlines


def weather_forecast(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER}"
    try:
        result = requests.get(url).json()
        weather = result["weather"][0]["main"]
        temperature = result["main"]["temp"]
        feels_like = result["main"]["feels_like"]
        return weather, f"{temperature}°C", f"{feels_like}°C"
    except Exception as e:
        print(e)
        return None, None, None
