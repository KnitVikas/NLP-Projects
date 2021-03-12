import os
import pandas as pd
import time
from gtts import gTTS
import pygame
import speech_recognition as sr

alphabets = [
"A",
"B",
"C",
"D",
"E",
"F",
"G",
"H",
"I",
"J",
"K",
"L",
"M",
"N",
"O",
"P",
"Q",
"R",
"S",
"T",
"U",
"V",
"W",
"x",
"Y",
"Z",
]

# conversation start
class AlphabetAssessment:

    def  __init__(self,alphabets):
        self.alphabets = alphabets
        print("Hi, this is for alphabet identification test")

# listening the speech and store in audio_text variable
    def speech(self,phrase_time_limit):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Talk")
            audio_text = r.listen(source, phrase_time_limit=phrase_time_limit)
            print("Time over, thanks")
        # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling

        try:
            # using google speech recognition
            print("We have recieved your voice.")
        except:
            print("Sorry, I did not get that")
        return r.recognize_google(audio_text)

    def speak(self,text):
        tts = gTTS(text=text, lang="en")
        filename = "audio1.mp3"
        tts.save(filename)
        pygame.mixer.init()
        pygame.mixer.music.load("audio1.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()
        os.remove(filename)

    def initial_conversation(self):
        sent1 = "Hi,I am Alex. What is your name ?"
        self.speak(sent1)
        try:
            name = self.speech(4)
        except:
            text = "pardon please !"
            self.speak(text)
            name = self.speech(4)
        sent2 = "Hi" + name + "I am from India. Where are you from ?"
        self.speak(sent2)

        try:
            place = self.speech(4)
        except:
            text = "pardon please !"
            place = self.speech(4)

        # Computer Selects accent recognition from the country could be identified
        sent3 = "You will be doing a Reading Assessment. That includes; identifying letter names and sounds, identifying sight words, reading one or more stories and then answering some questions. This is not a pass or fail kind of test so relax and do your best."
        self.speak(sent3)
        sent4 = "The test will begin In 1 minute Please prepare to identify the letters of the alphabet, Each letter will be displayed for 2 seconds"
        self.speak(sent4)

        # countdown for test start
        self.countdown(60)
        self.result_analysis()

    # define the countdown func.
    def countdown(self,TestStartTime):
        while TestStartTime:
            mins, secs = divmod(TestStartTime, 60)
            timer = "{:02d}:{:02d}".format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            TestStartTime -= 1

        print("Fire in the hole!!")
    # result analysis and table formation
    # OUTPUT AS :  a dictionary with key as alphabet shown and values as alphabets pronounced.
    def listen_alphabets(self,alphabets):
        result_alphabets = {}
        for alpha in self.alphabets:
            self.speak("say the name of letter only")
            # time.sleep(2)
            try:
                print(alpha)
                utter_alpha = self.speech(3)
            except:
                utter_alpha = "Not listen clearly"
            result_alphabets[alpha] = utter_alpha.upper()
            # if alpha == "E":
            #     break
        # print(result_alphabets)
        return result_alphabets
    
    def result_analysis(self):
        result = self.listen_alphabets(self.alphabets)
        # result = {"A": "A", "B": "Not listen clearly", "C": "y"}
        
        self.speak("Thank You")
        print("Here is your result", result)
        df = pd.DataFrame(result, columns=["Capital letters", "Response"])
        df["Capital letters"] = result.keys()
        df["Response"] = result.values()
        print("Response table : ", df)
        correct_response = 0
        No_Response = 0
        incorrect_responce = []
        for key in result.keys():
            if key == result[key]:
                correct_response += 1
            elif key == "Not listen clearly":
                No_Response += 1
            else:
                if len(key) == 1:
                    incorrect_responce.append(result[key].upper())

        listen_incorrect = len(alphabets) - No_Response - correct_response
        print("Total correct response :", correct_response)
        print("Total incorrect response :", " ", incorrect_responce, listen_incorrect)
        print("Total No response :", No_Response)

if __name__ == "__main__":
    obj = AlphabetAssessment(alphabets)
    obj.initial_conversation()
    