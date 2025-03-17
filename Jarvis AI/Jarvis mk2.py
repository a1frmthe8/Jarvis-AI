# Python program to translate speech to text and text to speech
import speech_recognition as sr
import pyttsx3
import os
from dotenv import load_dotenv
import openai

# Load API key from .env file
load_dotenv()
OPENAI_KEY = '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'

# Ensure the key is loaded properly
if not OPENAI_KEY:
    raise ValueError("OpenAI API Key is missing. Make sure it's set in the .env file.")

openai.api_key = OPENAI_KEY

# Function to convert text to speech
def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# Initialize the recognizer
r = sr.Recognizer()

def record_text():
    while True:
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                print("I'm listening...")

                # Listen for user's input
                audio2 = r.listen(source2)

                # Convert speech to text
                MyText = r.recognize_google(audio2)
                print(f"User said: {MyText}")

                return MyText.lower()
            
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

        except sr.UnknownValueError:
            print("Unknown error occurred, please try again.")

def send_to_chatGPT(messages, model="gpt-3.5-turbo"):
    try:
        client = openai.OpenAI(api_key=OPENAI_KEY)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=100,
            temperature=0.5,
        )
        return response.choices[0].message.content
    except openai.OpenAIError as e:
        if "insufficient_quota" in str(e):
            return "I have run out of OpenAI API quota. Please check billing or try again later."
        return f"Error communicating with OpenAI: {e}"
    
# Start conversation
messages = [{"role": "system", "content": "You are an AI assistant acting like Jarvis from Iron Man."}]

while True:
    text = record_text()

    # Exit condition
    if text in ["exit", "quit", "stop"]:
        print("Exiting...")
        SpeakText("Goodbye!")
        break

    messages.append({"role": "user", "content": text})
    response = send_to_chatGPT(messages)
    
    SpeakText(response)
    print(f"Jarvis: {response}")
