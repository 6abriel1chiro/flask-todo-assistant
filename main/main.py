# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 16:36:15 2021

@author: Gabriel Ichiro
"""

import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
listener = sr.Recognizer()
engine = pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen_command():
    try:
        with sr.Microphone() as source:
            print("escuchando... ")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'mavi' in command:
                command = command.replace('alexa', '')
                #print(command)
    except:
        pass
    return command

def runMavi():
    command = listen_command()
    if 'play' in command:
        song=command.replace('play', '')
        talk('playing' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('it is ' + time)
        print('it is ' + time)
    elif 'search' in command:
        search = command.replace('search', '')
        info = wikipedia.summary(search, 1)
        print(info)
        talk('found: ' + info)
    elif 'love you' in command:
        talk('thank you')
    elif 'do you love me' in command:
        talk('no')
    elif 'tell me something' in command:
        talk(pyjokes.get_joke())
    elif 'bye' in command:
        talk('bye then')
        exit(0)
    else:
        talk('I dont know what you are talking about')
while True:
    runMavi()
