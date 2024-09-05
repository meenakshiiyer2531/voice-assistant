import speech_recognition as sr
import pyttsx3
import requests
import time

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Converts text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listens for voice input and converts it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)  # Using Google Web API for speech recognition
        print(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand that.")
        return None
    except sr.RequestError:
        speak("Sorry, there was an issue with the speech recognition service.")
        return None

def process_command(command):
    """Processes the voice command."""
    if 'weather' in command:
        get_weather()
    elif 'your name' in command:
        speak("I am your voice assistant.")
    elif 'time' in command:
        current_time = time.strftime("%I:%M %p")
        speak(f"The time is {current_time}")
    elif 'exit' in command or 'bye' in command:
        speak("Goodbye!")
        exit()
    else:
        speak("I am not sure how to help with that.")

def get_weather():
    """Fetches the weather information using OpenWeatherMap API."""
    api_key = "your_openweather_api_key"  # Get your API key from https://openweathermap.org/
    city = "Bangalore"
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(weather_url).json()

    if response['cod'] == 200:
        weather_desc = response['weather'][0]['description']
        temperature = round(response['main']['temp'] - 273.15, 2)
        speak(f"The current weather in {city} is {weather_desc} with a temperature of {temperature} degrees Celsius.")
    else:
        speak("I couldn't retrieve the weather information right now.")

def wake_word_detection():
    """Simulates a wake word detection."""
    while True:
        speak("Say 'Hey meenu' to activate me.")
        command = listen()
        if command and 'hey meenu' in command:
            speak("How can I assist you?")
            return

# Main loop
if __name__ == "__main__":
    while True:
        wake_word_detection()  # Wait for wake word
        command = listen()  # Listen for the next command after wake word detection
        if command:
            process_command(command)
