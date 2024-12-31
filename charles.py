from random import choice
import time
import threading
import keyboard
import numpy as np
import pyttsx3
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
from conv import GEMINI_KEY, HOSTNAME, SCREEN_WIDTH,SCREEN_HEIGHT,farewell_text
from charles_button import CharlesButton
from utils import find_my_ip, get_news, search_on_google, search_on_wikipedia, send_email, weather_forecast, youtube
import google.generativeai as genai

genai.configure(api_key=GEMINI_KEY)
model=genai.GenerativeModel('gemini-1.5-flash')

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
            text='',
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
            readonly=False,
            background_color=(0,0,0,0),
            foreground_color=(1,1,1,1),
            size_hint_y=None,
            height=80,
            pos=(720,100),
            width=1200,
            font_name='static/teesri.otf',
        )        
        self.add_widget(self.subtitles_input)
        
        self.vrh=label.Label(
            text='',
            font_size=30,
            markup=True,
            font_name='static/dusri.ttf',
            pos=(1500,500)
            )
        self.add_widget(self.vrh)
        
        self.vlh=label.Label(
            text='',
            font_size=30,
            markup=True,
            font_name='static/dusri.ttf',
            pos=(400,500)
            )
        self.add_widget(self.vlh)
        self.add_widget(self.circle)
        
        self.engine = pyttsx3.init("sapi5")

        self.engine.setProperty('volume', 2)
        self.engine.setProperty('rate', 200)
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[0].id)
        
        self.listening=True
        
        keyboard.add_hotkey("`",self.start_recording)
        
    def speak(self,audio):        
        self.engine.say(audio)
        self.engine.runAndWait()
    
    def pause_listening(self):
        
        if self.listening:
            self.listening = False
            print("Listening paused...")
            self.speak(f"press ctrl+alt+k to resume from listening")
        else:
            self.listening = True
            print("Listening resumed...")
            self.speak(f"press ctrl+alt+k to pause from listening")
        
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
                self.speak("I didn't catch that. Could you repeat?")
                return ""
                
    def start_recording(self,*args):
        print("Recording has started")
        threading.Thread(target=self.run_speech_recognition).start()
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
        self.circle.pos = (SCREEN_WIDTH / 2 - self.circle.width / 2, SCREEN_HEIGHT / 2 - self.circle.height / 2)
            
            
    def update_volume(self,indata,frames,time,status):
        volume_norm = np.linalg.norm(indata) * 200
        self.volume = volume_norm
        self.volume_history.append(volume_norm)
        self.vrh.text = f'[b][color=3333ff]{np.mean(self.volume_history)}[/color][/b]'
        self.vlh.text = f'[b][color=3333ff]{np.mean(self.volume_history)}[/color][/b]'
        self.vlh.text = f'''[b][color=3344ff]
            {round(self.volume_history[0],7)}\n
            {round(self.volume_history[1],7)}\n
            {round(self.volume_history[2],7)}\n
            {round(self.volume_history[3],7)}\n
            {round(self.volume_history[4],7)}\n
            {round(self.volume_history[5],7)}\n
            {round(self.volume_history[6],7)}\n
            [/color][/b]'''
            
        self.vrh.text = f'''[b][color=3344ff]
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
        self.speak(choice(farewell_text))
        self.speak(f"This is {HOSTNAME} signing off")
        exit()
        
    def get_gemini_response(self,task):
        try:
            response=model.generate_content(task)
            return response            
        except Exception as e:
            print(f"Error: {e}")
            return "I am sorry"
            
    def handle_charles_commands(self, task):
        try:
            if "how are you" in task:
                self.respond_how_are_you()
            elif "open" in task:
                self.handle_open_commands(task)
            elif "search" in task:
                self.handle_search_commands(task)
            elif "email" in task:
                self.handle_email_command()
            elif "news" in task:
                self.handle_news_command()
            elif "weather" in task:
                self.handle_weather_command(task)
            elif "movie" in task:
                self.handle_movie_command()
            elif "ip" in task:
                self.handle_ip_command()
            elif "stop" in task or "exit" in task or "bye" in task:
                self.farewell()
            else:
                response = self.get_gemini_response(task)

                # Access the 'candidates' and extract the 'text' from the first candidate
                response_text = response.candidates[0].content.parts[0].text

                # Replace "*" if necessary
                response_text = response_text.replace("*", "")
                
                print(response)


                
                if response and response !="I am sorry":
                    self.speak(response)
                    
        except Exception as e:
            print(f"Error: {e}")

    def respond_how_are_you(self):
        self.speak("I am doing great, thank you for asking.")

    def handle_open_commands(self, task):
        if "command prompt" in task:
            self.speak("opening command prompt")
            os.system("start cmd")
        elif "powershell" in task:
            self.speak("opening powershell")
            os.system("start pwsh")
        elif "camera" in task:
            self.speak("opening camera")
            sp.run("start microsoft.windows.camera:", shell=True)
        elif "notepad" in task:
            self.speak("opening notepad")
            sp.Popen("notepad.exe")
        elif "calculator" in task:
            self.speak("opening calculator")
            os.system("start calc")
        elif "browser" in task:
            self.speak("opening browser")
            os.system("start brave")
        elif "google" in task:
            self.speak("opening google")
            os.system("start chrome")
        elif "file explorer" in task:
            self.speak("opening file explorer")
            os.system("start explorer")

    def handle_search_commands(self, task):
        if "search" in task:
            self.speak("What do you want to search")
            search = self.take_command()
            if search:
                search.lower()
                self.speak("searching...")
                self.speak(search_on_google(search))
        elif "wikipedia" in task:
            self.speak("What do you want to search on wikipedia?")
            search = self.take_command()
            if search:
                search.lower()
                self.speak("searching...")
                self.speak(f"According to Wikipedia,{search_on_wikipedia(search)}")
        elif "youtube" in task:
            self.speak("What do you want to watch on youtube?")
            video = self.take_command()
            if video:
                video.lower()
                self.speak("searching...")
                youtube(video)

    def handle_email_command(self):
        self.speak("To whom do you want to send the email?")
        self.speak("Enter in the Terminal")
        receiver = input("Enter the email address: ")
        self.speak("What is the subject of the email?")
        subject = input("Enter the subject: ").capitalize()
        self.speak("What is the message?")
        message = input("Enter the message: ").capitalize()
        if send_email(receiver, subject, message):
            self.speak("Email sent successfully!")
            print("Email sent successfully!")
        else:
            self.speak("Email could not be sent. Please check your credentials.")
            print("Email could not be sent. Please check your credentials.")

    def handle_news_command(self):
        news_headlines = get_news()
        self.speak("Here are the top news headlines:")
        self.speak("\n".join(news_headlines))

    def handle_weather_command(self, task):
        self.speak("What is the city name?")
        if "my" in task:
            ip_address = find_my_ip()
            city = requests.get(f"https://ipapi.co/{ip_address}/city").text
        else:
            city = self.take_command()
        self.speak(f"Fetching weather forecast for {city}")
        weather, temperature, feels_like = weather_forecast(city)
        self.speak(f"The weather is {weather} and the temperature is {temperature} and the feels like {feels_like}")
        with open("weather_forecast.txt", "w", encoding="utf-8") as file:
            file.write(f"Weather forecast for {city}:\n")
            file.write(f"The weather is {weather} and the temperature is {temperature} and the feels like {feels_like}")

    def handle_movie_command(self):
        movies_imdb = imdb.IMDb()
        self.speak("What is the name of the movie?")
        text = self.take_command()
        movies = movies_imdb.search_movie(text)
        self.speak(f"Searching...")
        self.speak(f"This is what I found for {text}")
        if movies:
            for movie in movies[:1]:
                title = movie.get("title", "Title not available")
                year = movie.get("year", "Year not available")
                self.speak(f"{title} ({year})")
                info = movie.getID()
                movie_info = movies_imdb.get_movie(info)
                rating = movie_info.get("rating", "Rating not available")
                cast = movie_info.get("cast", [])[:5]
                plot = movie_info.get("plot outline", "Plot summary not available")
                actor_names = ", ".join(actor["name"] for actor in cast) if cast else "Cast information not available"
                self.speak(f"Rating: {rating}")
                self.speak(f"The cast of the movie includes: {actor_names}")
                self.speak(f"The plot summary of the movie is: {plot}")
        else:
            self.speak(f"Sorry, I couldn't find any movie titled {text}.")

    def handle_ip_command(self):
        print("Your IP address is:", find_my_ip())
        self.speak(f"Your IP address is {find_my_ip()}")