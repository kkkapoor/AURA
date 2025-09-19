import os
import pathway as pw
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import playsound
import asyncio

translator = Translator()

# Define a Pathway component for retrieval (simulate RAG knowledge retrieval)
@pw.component
def retrieve_context(text: str) -> str:
    # Example retrieval logic; replace with real vector DB or index queries
    if "weather" in text.lower():
        return "Latest weather is sunny with occasional clouds."
    elif "news" in text.lower():
        return "Breaking news: AI is revolutionizing many industries."
    else:
        return "No relevant context found."

# Define a Pathway async component for translation using googletrans async API
@pw.component
async def translate_to_english(text: str) -> str:
    async with Translator() as translator_async:
        translation = await translator_async.translate(text, dest='en')
        return translation.text

# Define the main RAG speech processing pipeline as a Pathway graph
@pw.graph
async def speech_rag_pipeline(text: str) -> str:
    context = retrieve_context(text)
    translation = await translate_to_english(text)
    combined_text = f"{translation}. Context: {context}"
    return combined_text

# Function to listen to speech input
def listen_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language='hi-IN')
        print("You said (Hindi/English):", text)
        return text
    except Exception as e:
        print("Speech recognition error:", str(e))
        return ""

# Function to generate speech audio and play it
def speak_text(text):
    tts = gTTS(text, lang='en')
    filename = "temp_audio.mp3"
    tts.save(filename)
    abs_path = os.path.abspath(filename)
    playsound.playsound(abs_path, True)
    os.remove(abs_path)

def main():
    while True:
        text = listen_speech()
        if text:
            # Run the Pathway RAG pipeline synchronously, blocking until complete
            combined_output = pw.run(speech_rag_pipeline, text=text)
            print(f"Output: {combined_output}")
            speak_text(combined_output)

if __name__ == "__main__":
    main()