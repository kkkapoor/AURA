AURA – Real-time Hinglish to English Speech Translation
AURA is a real-time speech recognition and translation assistant. It can recognize Hindi, English, or Hinglish speech, translate it into English (or other target languages), and play the translated output using text-to-speech. The project includes a Flask backend for speech recognition and translation, a Pathway-based processing loop, and a Tailwind-powered frontend dashboard.

Features
🎤 Real-time speech capture using microphone.

🌐 Translation of Hindi, English, or Hinglish into English (US/UK) or Hindi.

🗣️ Automatic text-to-speech playback of translations.

⚡ Flask API with CORS-enabled frontend communication.

🎨 Beautiful TailwindCSS dashboard for interactive usage.

🔄 Pathway integration for UDF-based translation pipelines.

Project Structure
text
.
├── app.py                # Flask backend for speech recognition & translation
├── (Pathway Loop Code)   # Standalone script for CLI-based continuous listen/translate/speak
├── templates/
│   └── index.html        # Frontend Translation Dashboard (TailwindCSS + JS)
├── static/               # Optional static assets (CSS/JS if customized)
└── README.md             # Documentation
Installation
1. Clone Repository
bash
git clone https://github.com/your-username/aura-translation.git
cd aura-translation
2. Create Virtual Environment
bash
python3 -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
3. Install Dependencies
bash
pip install -r requirements.txt
If requirements.txt does not exist, create one with:

text
Flask
Flask-Cors
speechrecognition
pyaudio
deep-translator
gTTS
pydub
pathway
Running the Project
Option 1: Using Flask Backend + Frontend
Start the Flask server:

bash
python app.py
It runs on http://127.0.0.1:5000.

Open the frontend (index.html) in a browser.

Clicking the mic button starts recording speech.

The recognized text is sent to the backend API (/listen).

Translation is displayed and auto-played via speech synthesis.

Option 2: Using CLI Continuous Loop (Pathway-based)
Run the standalone main loop:

bash
python pathway_loop.py
(Adjust filename if integrated in app.py under main().)

The program will:

Listen from microphone.

Translate Hinglish/Hindi speech to English.

Speak the translated output.

Frontend Overview
Built with TailwindCSS for sleek, responsive UI.

Input/Output panels for speech and translation.

Dropdown selectors for source and target languages.

Mic button → starts recording via backend call.

Speaker buttons → play back recognized/translated text with correct TTS accent.

Example Workflow
User clicks mic button.

System records 5–7 seconds of speech.

Recognized Hindi/Hinglish is displayed in the Source box.

Translated English text is displayed in the Target box.

Speech synthesis auto-plays the translated output.

Requirements
Python 3.8+

Microphone access enabled

Browser with Web Speech API support (Chrome recommended)

Troubleshooting
Missing PyAudio:

bash
pip install pipwin
pipwin install pyaudio
No speech detected: Check microphone permissions.

Translation issues: Deep Translator may face API rate limits; retry or switch provider if needed.

Playback issues: Ensure system sound output is available (Windows users may need ffmpeg for pydub).

Roadmap
 Add multilingual target support beyond English/Hindi.

 Enable continuous streaming recognition instead of fixed chunks.

 Build Docker container for cross-platform deployment.

 Deploy backend on cloud and serve dashboard online.
