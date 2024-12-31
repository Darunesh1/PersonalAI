import pyttsx3
from datetime import datetime
from decouple import config
import requests
import wolframalpha
from conv import random_text, farewell_text
import speech_recognition as sr
from random import choice
import keyboard
import os
import subprocess as sp
import imdb

from utils import find_my_ip, get_news, search_on_google, search_on_wikipedia, send_email, weather_forecast, youtube

engine = pyttsx3.init("sapi5")

engine.setProperty('volume', 2)
engine.setProperty('rate', 200)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

USER = config('USER')
HOSTNAME = config('BOT')

listening = True



def pause_listening():
    global listening
    if listening:
        listening = False
        print("Listening paused...")
        speak(f"press ctrl+alt+k to resume from listening")
    else:
        listening = True
        print("Listening resumed...")
        speak(f"press ctrl+alt+k to pause from listening")
    
    


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
    elif 22 <= hour or hour < 6:
        speak(f"{USER}, you're not sleeping, are you?")
    speak(f"I am {HOSTNAME}, your assistant. How may I help you?")
    

def farewell():
    speak(choice(farewell_text))
    speak(f"This is {HOSTNAME} signing off")
    exit()
    
    
# Function to take command from user
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
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
# gree_me()
while True:
    if keyboard.is_pressed('ctrl+alt+k'):  # Check for pause/resume hotkey
        pause_listening()
        while keyboard.is_pressed('ctrl+alt+k'):  # Wait until key is released
            pass
    
    if keyboard.is_pressed('ctrl+alt+e'):  # Check for exit hotkey
        farewell()
        
    if listening:
        task = take_command()
        if task:  # Ensure task is not empty
            task = task.lower()
            if "how are you" in task:
                speak("I am doing great, thank you for asking.")
                
            elif "open command prompt" in task:
                speak("opening command prompt")
                os.system("start cmd")
                
            elif "open powershell" in task:
                speak("opening powershell")
                os.system("start pwsh")
                
            elif "open camera" in task:
                speak("opening camera")
                sp.run("start microsoft.windows.camera:",shell=True)
                
            elif "open notepad" in task:
                speak("opening notepad")
                sp.Popen("notepad.exe")
                
            elif "open calculator" in task:
                speak("opening calculator")
                os.system("start calc")
                
            elif "open browser" in task:
                speak("opening browser")
                os.system("start brave")
                
            elif "open google" in task:
                speak("opening google")
                os.system("start chrome")
                
            elif "open file explorer" in task:
                speak("opening file explorer")
                os.system("start explorer")
                
            elif "pause" in task:
                pause_listening()
                
            
                
            elif "search" in task:
                speak("What do you want to search")
                search = take_command()
                if search:
                    search.lower()                    
                    speak("searching...")
                    speak(search_on_google(search))
                
            elif "wikipedia" in task:
                speak("What do you want to search on wikipedia?")
                search = take_command()
                if search:
                    search.lower()                    
                    speak("searching...")
                    speak(f"According to Wikipedia,{search_on_wikipedia(search)}")
                
            elif "youtube" in task:
                speak("What do you want to watch on youtube?")
                video = take_command()
                if video:
                    video.lower()
                    speak("searching...")
                    youtube(video)
                    
            elif "email" in task:
                speak("To whom do you want to send the email?")
                speak("Enter in the Terminal")
                receiver = input("Enter the email address: ")
                speak("What is the subject of the email?")
                subject = input("Enter the subject: ").capitalize()
                speak("What is the message?")
                message = input("Enter the message: ").capitalize()
                
                if send_email(receiver, subject, message):
                    speak("Email sent successfully!")
                    print("Email sent successfully!")
                else:
                    speak("Email could not be sent. Please check your credentials.")
                    print("Email could not be sent. Please check your credentials.")
                    
            elif "news" in task:
                news_headlines = get_news()
                speak("Here are the top news headlines:")
                speak("\n".join(news_headlines))
                with open("news_headlines.txt", "w", encoding="utf-8") as file:
                    file.write("Top News Headlines:\n")
                    file.write("\n".join(news_headlines))
                    
            
                    
            elif "weather" in task:
                speak("What is the city name?")
                if "my" in task:
                    
                    ip_address = find_my_ip()
                    city=requests.get(f"https://ipapi.co/{ip_address}/city").text
                else:                    
                    city = take_command()
                
                speak(f"Fetching weather forecast for {city}")
                weather, temperature, feels_like = weather_forecast(city)
                speak(f"The weather is {weather} and the temperature is {temperature} and the feels like {feels_like}")
                with open("weather_forecast.txt", "w", encoding="utf-8") as file:
                    file.write(f"Weather forecast for {city}:\n")
                    file.write(f"The weather is {weather} and the temperature is {temperature} and the feels like {feels_like}")
                    
            elif "movie" in task:
                movies_imdb = imdb.IMDb()
                speak("What is the name of the movie?")
                text = take_command()
                movies = movies_imdb.search_movie(text)
                speak(f"Searching...")
                speak(f"This is what I found for {text}")

                if movies:
                    for movie in movies[:1]:  
                        title = movie.get("title", "Title not available")
                        year = movie.get("year", "Year not available")
                        speak(f"{title} ({year})")

                        # Get detailed information about the movie
                        info = movie.getID()
                        movie_info = movies_imdb.get_movie(info)

                        # Safely get fields with default values
                        rating = movie_info.get("rating", "Rating not available")
                        cast = movie_info.get("cast", [])[:5]
                        plot = movie_info.get("plot outline", "Plot summary not available")

                        # Extract actor names if cast is available
                        actor_names = ", ".join(actor["name"] for actor in cast) if cast else "Cast information not available"
                        speak(f"Rating: {rating}")
                        speak(f"The cast of the movie includes: {actor_names}")
                        speak(f"The plot summary of the movie is: {plot}")
                else:
                    speak(f"Sorry, I couldn't find any movie titled {text}.")
                    
            elif "calculate" in task:
                app_id=config("APP_ID")
                client = wolframalpha.Client(app_id)
                ind=task.lower().split().index('calculate')
                text=task.split()[ind+1:]
                result=client.query(''.join(text))
                try:
                    ans=next(result.results).text
                    speak("The answer is "+ans)
                    print("The answer is "+ans)
                except StopIteration:
                    speak("No results")
                    speak("please try again")
                    
            elif "what is" in task or "who is" in task or "where is" in task:
                app_id = config("APP_ID")
                client = wolframalpha.Client(app_id)

                try:
                    
                    if "what is" in task:
                        query = task.lower().split("what is", 1)[1].strip()
                    elif "who is" in task:
                        query = task.lower().split("who is", 1)[1].strip()
                    elif "where is" in task:
                        query = task.lower().split("where is", 1)[1].strip()
                    else:
                        query = None

                    if query:                        
                        result = client.query(query)
                        ans = next(result.results).text
                        speak("The answer is " + ans)
                        print("The answer is " + ans)
                    else:
                        speak("I am not sure what you are asking.")
                except StopIteration:
                    speak("No results found. Please try again.")
                except Exception as e:
                    speak("Something went wrong. Please try again.")
                    print(f"Error: {e}")


            
            elif "ip" in task:
                print("Your IP address is:", find_my_ip())
                speak(f"Your IP address is {find_my_ip()}")
                
            elif "stop" in task or "exit" in task or "bye" in task:
                farewell()
                
            else:
                speak(choice(random_text))
