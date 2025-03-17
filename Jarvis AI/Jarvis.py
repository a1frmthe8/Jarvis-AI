# Python program to translate
# Speech to text and text to speech
import speech_recognition as sr
import pyttsx3

import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_KEY = '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'

import openai
openai.api_key = OPENAI_KEY

#function to convert text to speech
def SpeakText(command):

    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# Initialize the recognizer
r = sr.Recognizer()

def record_text():
# Loop in case of errors
    while(1):
        try:
            # use the microphone as source for input.
            with sr.Microphone() as source2:

                # Prepare recognizer to receive input
                r.adjust_for_ambient_noise(source2, duration=0.2)

                print("I'm listening")

                # Listens for the user's input
                audio2 = r.listen(source2)

                # Using google to recognize audio
                MyText = r.recognize_google(audio2)

                return MyText
            
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknow error occurred")

def send_to_chatGPT(messages, model="gpt-1.0.0"):

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message

messages = [{"role": "user", "content": "Please act like Jarvis from Iron man."}]
while(1):
    text = record_text()
    messages.append({"role": "user", "content": text})
    response = send_to_chatGPT(messages)
    SpeakText(response)

    print(response)