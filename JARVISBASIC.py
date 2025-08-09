import speech_recognition as sr
import pyttsx3
import os
import datetime
import subprocess
import sys
import pywhatkit
import webbrowser
import requests
import pyautogui
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

API_KEY = "2aaf165581a4befd70fa64b979b724e6"  # Weather API Key

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
recognizer = sr.Recognizer()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# -----------------------
# Extra Feature Functions
# -----------------------
def google_search(query):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    speak(f"Searching Google for {query}")

def get_weather(city):
    try:
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(base_url, params=params)
        data = response.json()
        if data["cod"] != "404":
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            speak(f"The weather in {city} is {temp} degrees Celsius with {description}")
        else:
            speak("City not found.")
    except Exception as e:
        speak("Sorry, I couldn't get the weather right now.")

def open_path(path):
    try:
        if os.path.exists(path):
            os.startfile(path)
            speak(f"Opened {path}")
        else:
            speak("Path not found.")
    except Exception as e:
        speak("Sorry, I couldn't open the path.")

def take_screenshot():
    filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    pyautogui.screenshot().save(filename)
    speak(f"Screenshot saved as {filename}")

def set_volume(level):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level, None)
        speak(f"Volume set to {int(level*100)} percent")
    except Exception as e:
        speak("Sorry, I couldn't change the volume.")

def open_calendar():
    webbrowser.open("https://calendar.google.com/")
    speak("Opening Google Calendar")

# -----------------------
# Existing Functions
# -----------------------
def open_software(software_name):
    if 'chrome' in software_name:
        speak('Opening Chrome...')
        program = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        subprocess.Popen([program])
    elif 'microsoft edge' in software_name:
        speak('Opening Microsoft Edge...')
        program = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        subprocess.Popen([program])
    elif 'play' in software_name:
        speak('Opening YouTube')
        pywhatkit.playonyt(software_name)
    elif 'notepad' in software_name:
        speak('Opening Notepad...')
        subprocess.Popen(['notepad.exe']) 
    elif 'calculator' in software_name:
        speak('Opening Calculator...')
        subprocess.Popen(['calc.exe'])
    else:
        speak(f"I couldn't find the software {software_name}")

def close_software(software_name):
    if 'chrome' in software_name:
        speak('Closing Chrome...')
        os.system("taskkill /f /im chrome.exe")
    elif 'microsoft edge' in software_name:
        speak('Closing Microsoft Edge...')
        os.system("taskkill /f /im msedge.exe")
    elif 'notepad' in software_name:
        speak('Closing Notepad...')
        os.system("taskkill /f /im notepad.exe")
    elif 'calculator' in software_name:
        speak('Closing Calculator...')
        os.system("taskkill /f /im calculator.exe")
    else:
        speak(f"I couldn't find any open software named {software_name}")

def listen_for_wake_word():
    with sr.Microphone() as source:
        print('Listening for wake word...')
        while True:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            recorded_audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(recorded_audio, language='en_US').lower()
                if 'jarvis' in text:
                    print('Wake word detected!')
                    speak('Hi Puwan, How can I assist you?')
                    return True
            except:
                pass

def cmd():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print('Ask me anything...')
        recorded_audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(recorded_audio, language='en_US').lower()
        print('Your message:', text)
    except Exception as ex:
        print(ex)
        return

    if 'stop' in text:
        speak('Stopping the program. Goodbye!')
        sys.exit()

    # Existing features
    if 'open' in text:
        software_name = text.replace('open', '').strip()
        open_software(software_name)
    elif 'close' in text:
        software_name = text.replace('close', '').strip()
        close_software(software_name)
    elif 'time' in text:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        speak(current_time)
    elif 'who is god' in text:
        speak('Ajitheyyy Kadavuleyy')
    elif 'what is your name' in text:
        speak('My name is Jack, your Artificial Intelligence')

    # New features
    elif 'search about' in text:
        query = text.replace('search about', '').strip()
        google_search(query)
    elif "what's the weather in" in text or "weather in" in text:
        city = text.replace("what's the weather in", '').replace('weather in', '').strip()
        get_weather(city)
    elif 'open folder' in text or 'open file' in text:
        path = text.replace('open folder', '').replace('open file', '').strip()
        open_path(path)
    elif 'take screenshot' in text:
        take_screenshot()
    elif 'set volume to' in text:
        try:
            percent = int(text.replace('set volume to', '').replace('%', '').strip())
            set_volume(percent / 100)
        except:
            speak("Please say the volume as a number between 0 and 100.")
    elif 'open calendar' in text:
        open_calendar()

while True:
    if listen_for_wake_word():
        while True: 
            if cmd():
                break
