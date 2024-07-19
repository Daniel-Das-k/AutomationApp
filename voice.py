import speech_recognition as sr
from gtts import gTTS
import playsound

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def speak(self, text):
        tts = gTTS(text=text, lang='en')
        filename = 'voice.mp3'
        tts.save(filename)
        playsound.playsound(filename)

    def get_audio(self):
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)
            said = ""

            try:
                said = self.recognizer.recognize_google(audio)
                print(said)
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))

        return said.lower()

