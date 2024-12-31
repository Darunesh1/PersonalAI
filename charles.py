from random import choice
import time
import threading
import keyboard
import numpy as np
import requests
import sounddevice as sd
import speech_recognition as sr
import os
import pyautogui
import subprocess as sp
import webbrowser
import imdb
from kivy.uix import widget,image,label,boxlayout,textinput
from kivy import clock
from conv import HOSTNAME, SCREEN_WIDTH,SCREEN_HEIGHT,farewell_text
from charles_button import CharlesButton
from utils import find_my_ip, get_news, search_on_google, search_on_wikipedia, send_email, speak, weather_forecast, youtube

class Charles(widget.Widget):
    def __init__(self,**kwargs):
        super(Charles,self).__init__(**kwargs)
        self.volume = 0
        self.volume_history = [0,0,0,0,0,0,0]
        self.volume_history_size = 140
        
        self.min_size=0.2*SCREEN_WIDTH
        self.max_size=0.8*SCREEN_WIDTH
        
        self.add_widget(image.Image(source='static/boarder.eps.png',size=(1920,1080)))
        self.circle=CharlesButton(size=(284.0,284.0),background_normal='static/circle.png')
        self.circle.bind(on_press=self.start_recording)
        
        self.start_recording()
        
        self.add_widget(image.Image(
            source='static/charles.gif',
            size=(self.min_size,self.min_size), 
            pos = (SCREEN_WIDTH / 2 - self.min_size / 2 , SCREEN_HEIGHT / 2 - self.min_size / 2))
            )
        
        time_layout=boxlayout.BoxLayout(
            orientation='vertical',
            pos=(150,900)
            )
        
        self.time_label= label.Label(
            text='00:00:00',
            font_size=30,
            markup=True,
            font_name='static/mw.ttf'
            )        
        time_layout.add_widget(self.time_label)
        self.add_widget(time_layout)
        
        clock.Clock.schedule_interval(self.update_time,1)
        
        self.title = label.Label(
            text='[b][color=3333ff]DARRIOUR[/color][/b]',
            font_size=30,
            markup=True,
            font_name='static/dusri.ttf',
            pos=(150,1000)
            )
        self.add_widget(self.title)
        
        self.subtitles_input = textinput.TextInput(
            text='HI idiots',
            font_size=30,
            readonly=True,
            background_color=(0,0,0,0),
            foreground_color=(0,0,0,1),
            size_hint_y=None,
            height=80,
            pos=(720,100),
            width=1200,
            font_name='static/teesri.otf',
        )        
        self.add_widget(self.subtitles_input)
        
        self.vrh=label.Label(
            text='[b][color=3333ff]VOLUME[/color][/b]',
            font_size=30,
            markup=True,
            font_name='static/dusri.ttf',
            pos=(150,800)
            )
        self.add_widget(self.vrh)
        
        self.vlh=label.Label(
            text='[b][color=3333ff]VOLUME[/color][/b]',
            font_size=30,
            markup=True,
            font_name='static/dusri.ttf',
            pos=(150,800)
            )
        self.add_widget(self.vlh)
        self.add_widget(self.circle)
        
        keyboard.add_hotkey("ctrl+alt+k",self.start_recording)
        
    def take_command(self):        
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
                return ""
                
    def start_recording(self,*args):
        print("Recording has started")
        threading.Thread(target=self.run_speech_recognition).start
        print("recording ended")
            
    def run_speech_recognition(self):
        print('before speech rec obj')
        r= sr.Recognizer()
        with sr.Microphone() as source:
            print('after speech rec obj')
            audio=r.listen(source)
            print('after audio obj')
        print("after speech rec obj")
        
        try:
            task=r.recognize_google(audio,language="en-in")
            print(f"Recognised:{task}")
            clock.Clock.schedule_once(lambda dt: setattr(self.subtitles_input,'text',task))
            self.handle_charles_commands(task.lower())
        except sr.UnknownValueError:
            print("Google speech recognition could not understand audio")
            
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
    def update_time(self,dt):
        current_time=time.strftime('TIME\n\t\%H:%M:%S')
        self.time_label.text = f'[b][color=3333ff]{current_time}[/color][/b]'
            
    def update_circle(self,dt):
        try:
            self.size_value = int(np.mean(self.volume_history))
            
        except Exception as e:
            self.size_value = self.min_size
            print('Warning:',e)
            
        if self.size_value <= self.min_size:
            self.size_value = self.min_size
        elif self.size_value >= self.max_size:
            self.size_value = self.max_size
        self.circle.size = (self.size_value,self.size_value)
        self.circle.pos = (SCREEN_WIDTH / 2 - self.min_size / 2 , SCREEN_HEIGHT / 2 - self.min_size / 2)
            
            
    def update_volume(self,indata,frames,time,status):
        volume_norm = np.linalg.norm(indata) * 200
        self.volume = volume_norm
        self.volume_history.append(volume_norm)
        self.vrh.text = f'[b][color=3333ff]{np.mean(self.volume_history)}[/color][/b]'
        self.vlh.text = f'[b][color=3333ff]{np.mean(self.volume_history)}[/color][/b]'
        self.vlh.text = f'''[b][color=3333ff]
            {round(self.volume_history[0],7)}\n
            {round(self.volume_history[1],7)}\n
            {round(self.volume_history[2],7)}\n
            {round(self.volume_history[3],7)}\n
            {round(self.volume_history[4],7)}\n
            {round(self.volume_history[5],7)}\n
            {round(self.volume_history[6],7)}\n
            [/color][/b]'''
        self.vrh.text = f'''[b][color=3333ff]
            {round(self.volume_history[0],7)}\n
            {round(self.volume_history[1],7)}\n
            {round(self.volume_history[2],7)}\n
            {round(self.volume_history[3],7)}\n
            {round(self.volume_history[4],7)}\n
            {round(self.volume_history[5],7)}\n
            {round(self.volume_history[6],7)}\n
            [/color][/b]'''
            
        if len(self.volume_history) > self.volume_history_size:
            self.volume_history.pop(0)
                
    def start_listening(self):
        self.stream = sd.InputStream(callback=self.update_volume)
        self.stream.start()
        
    def farewell(self):
        speak(choice(farewell_text))
        speak(f"This is {HOSTNAME} signing off")
        exit()
            
    def handle_charles_command(self,task):
        try:
            task = self.take_command()
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
                    search = self.take_command()
                    if search:
                        search.lower()                    
                        speak("searching...")
                        speak(search_on_google(search))
                    
                elif "wikipedia" in task:
                    speak("What do you want to search on wikipedia?")
                    search = self.self.take_command()
                    if search:
                        search.lower()                    
                        speak("searching...")
                        speak(f"According to Wikipedia,{search_on_wikipedia(search)}")
                    
                elif "youtube" in task:
                    speak("What do you want to watch on youtube?")
                    video = self.take_command()
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
                    
                        
                
                        
                elif "weather" in task:
                    speak("What is the city name?")
                    if "my" in task:
                        
                        ip_address = find_my_ip()
                        city=requests.get(f"https://ipapi.co/{ip_address}/city").text
                    else:                    
                        city = self.take_command()
                    
                    speak(f"Fetching weather forecast for {city}")
                    weather, temperature, feels_like = weather_forecast(city)
                    speak(f"The weather is {weather} and the temperature is {temperature} and the feels like {feels_like}")
                    with open("weather_forecast.txt", "w", encoding="utf-8") as file:
                        file.write(f"Weather forecast for {city}:\n")
                        file.write(f"The weather is {weather} and the temperature is {temperature} and the feels like {feels_like}")
                        
                elif "movie" in task:
                    movies_imdb = imdb.IMDb()
                    speak("What is the name of the movie?")
                    text = self.take_command()
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
                        
                


                
                elif "ip" in task:
                    print("Your IP address is:", find_my_ip())
                    speak(f"Your IP address is {find_my_ip()}")
                    
                elif "stop" in task or "exit" in task or "bye" in task:
                    self.farewell()
                    
                else:
                    speak(choice(random_text))
        except Exception as e:
            print(f"Error: {e}")