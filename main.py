import datetime
import speech_recognition as sr


# Function to recognize speech using the Google Speech Recognition API
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}\n")

    except Exception as e:
        print("No audio detected:", e)
        return ""
    return query


# Function to perform tasks based on user speech input
def main():
    while True:
        query = get_audio()
        if "hello" in query.lower():
            print("Hello! How can I help you?")

        elif "what time is it" in query.lower():
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"The current time is {current_time}")

        elif "what date is it" in query.lower():
            current_date = datetime.datetime.now().strftime("%d-%m-%Y")
            print(f"The current date is {current_date}")

        elif "search" in query.lower():
            search_query = query.split("search")[-1].strip()
            print(f"Searching for '{search_query}' on the web...")
            # Replace this line with actual web search code
            # Here's a dummy print statement to simulate the web search result
            print(f"Result 1: Dummy search result 1 for '{search_query}'")
            print(f"Result 2: Dummy search result 2 for '{search_query}'")

        else:
            print("Sorry, I didn't catch that. Could you please repeat your query?")


if __name__ == "__main__":
    main()
