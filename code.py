import speech_recognition as sr

def listen_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        # recognize speech (bilingual Hindi + English)
        text = recognizer.recognize_google(audio, language='hi-IN')
        print("You said (Hindi/English):", text)
        return text
    except Exception as e:
        print("Error recognizing speech:", str(e))
        return ""

from googletrans import Translator
import pathway as pw

translator = Translator()

def translate_to_english(text):
    translation = translator.translate(text, dest='en')
    return translation.text

def process_speech_stream():
    graph = pw.Graph()

    @graph.node
    def speech_processing_node(text: str) -> str:
        print(f"Original Text: {text}")
        translated_text = translate_to_english(text)
        print(f"Translated Text: {translated_text}")
        return translated_text

    stream = graph.stream()
    stream.connect(speech_processing_node)

    return graph, stream

from gtts import gTTS
import playsound
import os

def speak_text(text):
    tts = gTTS(text, lang='en')
    filename = "temp_audio.mp3"
    tts.save(filename)
    playsound.playsound(filename, True)
    os.remove(filename)

def main():
    graph, stream = process_speech_stream()

    while True:
        text = listen_speech()
        if text:
            stream.send(text)
            translated_text = translate_to_english(text)  # Can get from Pathway node stream alternatively
            speak_text(translated_text)

if __name__ == "__main__":
    main()