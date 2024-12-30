import pyttsx3 


engine = pyttsx3.init("sapi5")

# engine.say("        hi there i am your assistant")
# engine.runAndWait()

engine.setProperty('volume', 1)
engine.setProperty('rate', 130)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
    
speak(" hi there, i am your assistant")
print("Hi there, I am your assistant")