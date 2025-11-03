import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import musicLibrary
from gtts import gTTS
import google.generativeai as genai
import pygame
import os


recognizer = sr.Recognizer()
engine = pyttsx3.init()

engine.setProperty('rate', 180)
newsapi = os.getenv("NEWS_API_KEY")

def speak_old(text):
    engine.say(text)
    engine.runAndWait()


def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 


# For AI Processing..
genai.configure(api_key=os.getenv("OPENAI_API_KEY"))

def aiProcess(command):
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"""
                You are Jarvis, a calm and intelligent AI voice assistant.
                Respond in short sentences, be helpful, clear, and friendly.
                Do not write long paragraphs.
                User: {command}
                Jarvis:
            """
    response = model.generate_content(prompt)
    return response.text.strip()


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().replace("play", "").strip()  # Extract full song name
        if song in musicLibrary.music:
            webbrowser.open(musicLibrary.music[song])
            speak(f"Playing {song}")
        else:
            speak("Song not found in your library.")


    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])

        else:
            speak("I cannot fetch news without an API key.")

    else:
        # Let AI handle the request
        output = aiProcess(c)
        speak(output) 



if __name__ == "__main__":
    speak("Initializing Jarvis....")
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)  

    while True:
        try:
            with mic as source:
                print("Say 'Jarvis' to activate...")
                audio = recognizer.listen(source)

            text = recognizer.recognize_google(audio).lower()
            print("Heard:", text)

            if "jarvis" in text:
                speak("Yes?")

                with mic as source:
                    recognizer.adjust_for_ambient_noise(source)
                    print("Listening for command...")
                    audio = recognizer.listen(source)

                command = recognizer.recognize_google(audio)
                print("Command:", command)
                processCommand(command)

        except Exception:
            pass 
