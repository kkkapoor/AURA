import os
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play


'''# Context retrieval (simple function now)
def retrieve_context(text: str) -> str:
    if "weather" in text.lower():
        return "Latest weather is sunny with occasional clouds."
    elif "news" in text.lower():
        return "Breaking news: AI is revolutionizing many industries."
    else:
        return "No relevant context found."
'''


# Translate text to English
def translate_to_english(text: str) -> str:
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        print("Translation error:", str(e))
        return text


# Main pipeline
def speech_rag_pipeline(text: str) -> str:
    #context = retrieve_context(text)
    translation = translate_to_english(text)
    combined_text = f"{translation}"
    #. Context: {context}"
    return combined_text


# Listen to speech
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


# Speak text
def speak_text(text):
    tts = gTTS(text, lang='en')
    filename = "temp_audio.mp3"
    tts.save(filename)
    sound = AudioSegment.from_mp3(filename)
    play(sound)
    os.remove(filename)


# Main loop
def main():
    while True:
        text = listen_speech()
        if text:
            combined_output = speech_rag_pipeline(text)
            print(f"Output: {combined_output}")
            speak_text(combined_output)


if __name__ == "__main__":
    main()
