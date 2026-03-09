# BuiltIn Imports
import datetime
import os
import smtplib
import ssl
import time
import webbrowser
from email.message import EmailMessage
from urllib.parse import quote_plus

# Third-Party Imports
import pyautogui
import pyttsx3
import pywhatkit
import requests
import speech_recognition as sr
import wikipedia
from dotenv import load_dotenv

load_dotenv()

# ? Helper function to create a new pyttsx3 engine instance
def _build_tts_engine():
    """Create and configure a pyttsx3 engine instance.
    For each utterance to avoid SAPI deadlocks after
    microphone usage."""
    tts_engine = pyttsx3.init()
    voices = tts_engine.getProperty("voices")
    if voices:
        tts_engine.setProperty("voice", voices[0].id)
    return tts_engine

# ? Function to convert text to speech
def speak(text):
    print("Assistant:", text)
    if not text:
        return

    try:
        # * Recreate engine per utterance to avoid SAPI deadlocks after microphone usage.
        tts_engine = _build_tts_engine()
        tts_engine.say(str(text))
        tts_engine.runAndWait()
        tts_engine.stop()
    except Exception as e:
        print("TTS engine error:", e)

# ? Function to greet the user based on the current time of day
def wish_user():
    hour = datetime.datetime.now().hour
    greeting = (
        "Good morning!"
        if 5 <= hour < 12
        else "Good afternoon!" if 12 <= hour < 18 else "Good evening!"
    )
    speak(f"{greeting} How can I assist you?")

# ? Function to listen for user commands and return the recognized text
def listen_command():
    # Initialize the speech recognition engine
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            # Calibrate for background noise
            r.adjust_for_ambient_noise(source, duration=1)
            r.pause_threshold = 1
            audio = r.listen(source)
    except OSError as e:
        print("Microphone is not available on this device.", e)
        return None
    except Exception as e:
        print("Unable to capture audio input.", e)
        return None

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

# ? Function to search the web using the default browser
def search_web(query):
    speak(f"Searching for {query} on the web...")
    url = "https://www.google.com/search?q=" + query
    webbrowser.open(url)

# ? Function to open a specified websites
def open_site(site):
    speak(f"Opening {site}...")
    if site == "youtube":
        webbrowser.open("https://www.youtube.com")
    elif site == "google":
        webbrowser.open("https://www.google.com")
    elif site == "github":
        webbrowser.open("https://www.github.com")
    elif site == "stackoverflow":
        webbrowser.open("https://stackoverflow.com")
    elif site == "gmail":
        webbrowser.open("https://mail.google.com")
    else:
        speak(
            "Sorry, I can only open YouTube, Google, GitHub, StackOverflow, and Gmail at the moment."
        )

# ? Function to open specified applications
def open_app(app):
    speak(f"Opening {app}...")
    if app == "notepad":
        os.system("notepad.exe")
    elif app == "calculator":
        os.system("calc.exe")
    elif app == "chrome":
        os.system("start chrome")
    elif app == "explorer":
        os.system("explorer.exe")
    elif app == "excel":
        os.system("start excel")
    elif app == "word":
        os.system("start winword")
    elif app == "powerpoint":
        os.system("start powerpnt")
    elif app == "spotify":
        try:
            os.system("start spotify")
        except Exception as e:
            speak("Sorry, the Spotify app not present.")
            print("Open app error:", e)
    else:
        speak(
            "Sorry, I can only open Notepad, Calculator, Chrome, and Spotify at the moment."
        )

# ? Function to search Wikipedia and return a summary of the topic
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

# ? Function to get the current weather for a specified city using OpenWeatherMap API
def get_weather():
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        speak("Weather API key is missing in environment variables.")
        return None
    speak("Which city's weather would you like to know?")
    city_name = listen_command()
    if not city_name:
        speak("I didn't catch the city name. Please try again.")
        return None
    safe_city = quote_plus(city_name.strip())
    url = (
        f"http://api.openweathermap.org/data/2.5/weather?q={safe_city}&appid={api_key}"
    )
    try:
        response = requests.get(url, timeout=5).json()
        weather = response.get("weather")
        main_data = response.get("main")
        if not weather or not main_data:
            speak("Sorry, I couldn't fetch weather details for that city.")
            return None

        weather_description = weather[0]["description"]
        temperature = main_data["temp"]
        temperature = temperature - 273.15  # Convert from Kelvin to Celsius
        temperature = round(temperature, 2)
        speak(
            f"The temperature in {city_name} is {temperature} degrees Celsius. And the weather is {weather_description}."
        )
    except (requests.exceptions.RequestException, KeyError, TypeError, ValueError) as e:
        print("Error fetching weather data:", e)
        speak(
            "Sorry, I couldn't fetch the weather. Please check your internet connection."
        )

# ? Function to send an email using SMTP protocol
def send_email(to, subject, body):
    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")
    if not sender_email or not sender_password:
        speak("Email credentials are missing in environment variables.")
        return

    speak("Who should I send the email to?")
    speak("Please provide the recipient's email address.")
    to_email = listen_command()
    if not to_email or "@" not in to_email:
        speak("Invalid email address.")
        return

    speak("What is the subject?")
    subject = listen_command()
    speak("What is the body of the email?")
    body = listen_command()
    if not to_email and not subject and not body:
        speak("I didn't catch the email details. Please try again.")

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        speak("Email has been sent successfully!")
    except Exception as e:
        speak("Failed to send email.")
        print(f"Error: {e}")

# ? Function to play music based on the user's command
def play_music(query):
    try:
        if "spotify" in query:
            speak("Opening Spotify...")
            webbrowser.open("https://www.spotify.com/")
        else:
            speak("Which song?")
            song = listen_command()
            if song:
                speak("Playing music...")
                pywhatkit.playonyt(song)
            else:
                speak("Song not found.")
    except Exception as e:
        print("Sorry, I couldn't play the music.",e)
        speak("Sorry, I couldn't play the music. Please try again later.")

# ? Function to send a WhatsApp message using pywhatkit
def send_whatsapp():
    speak("Enter phone number with country code.")
    number = listen_command()
    speak("What message?")
    message = listen_command()

    if number and message:
        pywhatkit.sendwhatmsg_instantly(f"+{number}", message)
        speak("Message sent.")

# ? Function to take a screenshot and save it as a file
def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save(f"screenshot{time.time()}.png")
    speak("Screenshot saved.")

# ? Function to calculate a mathematical expression using eval
def calculate(expression):
    try:
        # Use a restricted namespace with only safe math operations
        safe_dict = {"__builtins__": {}}
        result = eval(expression, safe_dict)
        speak(f"The result is {result}")
    except Exception:
        speak("Invalid calculation.")

# ? Function to process the user's command and execute corresponding actions
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
    elif "weather" in command:
        get_weather()
    elif "play" in command:
        play_music(command)
    elif "screenshot" in command:
        take_screenshot()
    elif "calculate" in command:
        expression = command.replace("calculate", "")
        calculate(expression)
    elif "send" in command:
        if "email" in command:
            send_email()
        elif "whatsapp" in command:
            send_whatsapp()
        else:
            speak("Sorry, I can only send emails at the moment.")
    elif "open" in command:
        if "app" in command:
            app = command.split("app")[-1].strip()
            open_app(app)
        elif "website" in command:
            site = command.split("website")[-1].strip()
            open_site(site)
        else:
            speak("Sorry, I can only open websites at the moment.")
    elif "search" in command:
        if "on wikipedia" in command:
            search_query = command.replace("wikipedia", "").strip()
            search_wikipedia(search_query)
        else:
            search_query = command.split("search")[-1].strip()
            search_web(search_query)
    elif "exit" in command or "stop" in command:
        hour = datetime.datetime.now().hour
        if 19 <= hour < 24 or 0 <= hour < 5:
            speak("Good night!")
        else:
            speak("Goodbye!")
        exit()
    else:
        speak("Sorry, I didn't catch that. Can you please repeat?")

# Main program
def main():
    wish_user()
    while True:
        command = listen_command()
        if command:
            process_command(command)

if __name__ == "__main__":
    main()
