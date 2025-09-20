import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import pathway as pw
import os

# -------------------------------
# Pathway UDF for translation
# -------------------------------
@pw.udf
def translate_text(text: str) -> str:
    """
    Translate mixed Hindi/English text to English.
    """
    try:
        # Translate whole sentence at once to preserve meaning
        translation = GoogleTranslator(source='auto', target='en').translate(text)
        return translation[0].upper() + translation[1:] if translation else translation
    except Exception as e:
        print("Translation error:", str(e))
        return text

# -------------------------------
# Speech recognition
# -------------------------------
def listen_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source, phrase_time_limit=7)
    try:
        text = recognizer.recognize_google(audio, language='hi-IN')
        print("You said (Hindi/English):", text)
        return text
    except Exception as e:
        print("Speech recognition error:", str(e))
        return ""

# -------------------------------
# Speak output
# -------------------------------
def speak_text(text: str):
    if not text.strip():
        return
    tts = gTTS(text, lang='en')
    filename = "temp_audio.mp3"
    tts.save(filename)
    sound = AudioSegment.from_mp3(filename)
    play(sound)
    os.remove(filename)

# -------------------------------
# Main loop
# -------------------------------
def main():
    while True:
        text = listen_speech()
        if text:
            # Use Pathway UDF directly
            translation_str = translate_text.__wrapped__(text)
            print(f"Output (English): {translation_str}")
            speak_text(translation_str)

if __name__ == "__main__":
    main()
