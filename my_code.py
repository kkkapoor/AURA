import networkx as nx
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import playsound
import os

translator = Translator()

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

def translate_to_english(text):
    translation = translator.translate(text, dest='en')
    return translation.text

def speak_text(text):
    tts = gTTS(text, lang='en')
    filename = "temp_audio.mp3"
    tts.save(filename)
    playsound.playsound(filename, True)
    os.remove(filename)

def process_speech_stream():
    graph = nx.DiGraph()

    def speech_processing_node(text: str) -> str:
        print(f"Original Text: {text}")
        translated_text = translate_to_english(text)
        print(f"Translated Text: {translated_text}")
        return translated_text

    graph.add_node('speech_processing_node', func=speech_processing_node)

    return graph

def run_pipeline(graph, input_texts):
    for text in input_texts:
        node_func = graph.nodes['speech_processing_node']['func']
        output = node_func(text)
        speak_text(output)

def main():
    graph = process_speech_stream()

    while True:
        text = listen_speech()
        if text:
            run_pipeline(graph, [text])

if __name__ == "__main__":
    main()
