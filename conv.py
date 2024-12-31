import os

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

NEWS = os.environ.get("NEWS")
WEATHER = os.environ.get("WEATHER")
APP_ID = os.environ.get("APP_ID")

IP_URL='https://api.ipify.org?format=json'

NEWS_URL="https://newsdata.io/api/1/latest"

WEATHER_URL="https://api.openweathermap.org/data/2.5/weather"

SMTP_URL="smtp.gmail.com"
SMTP_PORT=587

