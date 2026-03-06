import os
import datetime
import requests
import wikipedia
import webbrowser
import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv
load_dotenv()

# Initialize text-to-speech engine
engine = pyttsx3.init()
# Set the default voice for text-to-speech synthesis
voices = engine.getProperty('voices')
# Change the index to use a different voice if needed
engine.setProperty('voice', voices[0].id)


# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to greet the user based on the current time of day
def wish_user():
    hour = datetime.datetime.now().hour
    greeting = "Good morning!" if 5 <= hour < 12 else "Good afternoon!" if 12 <= hour < 18 else "Good evening!"
    speak(f"{greeting} How can I assist you?")

# Function to listen for user commands and return the recognized text
def listen_command():
    # Initialize the speech recognition engine
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        # Calibrate for background noise
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-US")
        print(f"You said: {query}\n")
        return query
    except sr.UnknownValueError as e:
        print("I'm sorry, I couldn't understand your command. Please try again.", e)
        return None
    except sr.RequestError as e:
        print("Sorry, there was an issue with the speech recognition service.", e)
        return None

# Function to process the user's command and execute corresponding actions
def process_command(command):
    command = command.lower()

    if "hello" in command:
        speak("Hello there!")
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {current_time}")
    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%d-%m-%Y")
        speak(f"The current date is {current_date}")
    elif 'open' in command:
        if 'youtube' in command:
            webbrowser.open("youtube.com")
        elif 'google' in command:
            webbrowser.open("google.com") 
        else:
            speak("Sorry, I can only open YouTube and Google at the moment.")
    elif "search" in command:
        if 'on wikipedia' in command:
            search_query = command.replace("wikipedia", "").strip()
            search_wikipedia(search_query)
        else:
            search_query = command.split("search")[-1].strip()
            search_web(search_query)
    elif "exit" or "stop" in command:
        hour = datetime.datetime.now().hour
        if 19 <= hour < 24 or 0 <= hour < 5:
            speak("Good night!")
        else:
            speak("Goodbye!")
        exit()
    else:
        speak("Sorry, I didn't catch that. Can you please repeat?")

# Function to search the web using the default browser
def search_web(query):
    speak(f"Searching for {query} on the web...")
    url = "https://www.google.com/search?q=" + query
    webbrowser.open(url)


# Function to search Wikipedia and return a summary of the topic
def search_wikipedia(query):
    speak(f"Searching Wikipedia for {query}...")
    try:
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
    except wikipedia.exceptions.DisambiguationError:
        speak("Multiple Wikipedia results found. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("No Wikipedia results found.")
    except Exception as e:
        speak("Sorry, I couldn't find any information on this topic.")
        print("Sorry, I couldn't find any information on this topic.", e)
    # pass

# Main program
if __name__ == "__main__":
    wish_user()
    while True:
        command = listen_command()
        if command:
            process_command(command)
