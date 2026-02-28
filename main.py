import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to greet the user based on the current time of day
def wish_user():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("How can I assist you?")

# Function to listen for user commands and return the recognized text
def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-US")
        print(f"You said: {query}\n")
        return query
    except Exception as e:
        print("I'm sorry, I couldn't understand your command. Please try again.", e)
        return ""

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
    elif "search" in command:
        search_query = command.split("search")[-1].strip()
        search_web(search_query)
    else:
        speak("I'm sorry, I couldn't understand your command.")

# Function to search the web using the default browser
def search_web(query):
    speak(f"Searching for {query} on the web...")
    url = "https://www.google.com/search?q=" + query
    webbrowser.open(url)


# Main program
if __name__ == "__main__":
    wish_user()
    while True:
        command = listen_command()
        if command:
            process_command(command)
