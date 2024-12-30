import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config

EMAIL=""
PASSWORD=""
NEWS=config("NEWS_API_KEY")


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
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey=a786fe7ae43e4bb7b2f314d2337dbea7"
    result = requests.get(url).json()
    
    articles = result["articles"]
    for article in articles:
        news_headlines.append(article["title"])
    return news_headlines[:4]