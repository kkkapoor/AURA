import os
import json
import time
import uuid
import random

# Sample phrases in different languages
SAMPLE_PHRASES = {
    "fr": [
        "Bonjour, comment ça va?",
        "Je ne comprends pas ce mot",
        "Pouvez-vous m'aider avec cette traduction?",
        "Merci beaucoup pour votre aide",
        "Comment dit-on 'meeting' en français?"
    ],
    "hi": [
        "नमस्ते, आप कैसे हैं?",
        "मुझे यह शब्द समझ नहीं आया",
        "क्या आप इस अनुवाद में मेरी मदद कर सकते हैं?",
        "आपकी सहायता के लिए बहुत धन्यवाद",
        "अंग्रेजी में 'बैठक' कैसे कहते हैं?"
    ],
    "bn": [
        "হ্যালো, আপনি কেমন আছেন?",
        "আমি এই শব্দটি বুঝতে পারছি না",
        "আপনি কি এই অনুবাদে আমাকে সাহায্য করতে পারেন?",
        "আপনার সাহায্যের জন্য অনেক ধন্যবাদ",
        "ইংরেজিতে 'সভা' কীভাবে বলা হয়?"
    ],
    "es": [
        "Hola, ¿cómo estás?",
        "No entiendo esta palabra",
        "¿Puedes ayudarme con esta traducción?",
        "Muchas gracias por tu ayuda",
        "¿Cómo se dice 'reunión' en inglés?"
    ],
    "de": [
        "Hallo, wie geht es dir?",
        "Ich verstehe dieses Wort nicht",
        "Kannst du mir bei dieser Übersetzung helfen?",
        "Vielen Dank für deine Hilfe",
        "Wie sagt man 'meeting' auf Deutsch?"
    ]
}

def generate_input_data(input_dir="./input_data", interval=2.0, num_samples=10):
    """
    Generate sample input data files to simulate real-time data ingestion.
    
    Args:
        input_dir: Directory to write input files
        interval: Time interval between generating samples (seconds)
        num_samples: Number of samples to generate
    """
    os.makedirs(input_dir, exist_ok=True)
    
    session_id = str(uuid.uuid4())
    
    for i in range(num_samples):
        # Select a random language
        language = random.choice(list(SAMPLE_PHRASES.keys()))
        
        # Select a random phrase in that language
        text = random.choice(SAMPLE_PHRASES[language])
        
        # Create data entry
        data = {
            "text": text,
            "timestamp": time.time(),
            "session_id": session_id
        }
        
        # Write to a unique file
        filename = f"{input_dir}/input_{int(time.time())}_{i}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        
        print(f"Generated input: {text} (Language: {language})")
        
        # Wait for the specified interval
        time.sleep(interval)
    
    print(f"Generated {num_samples} input samples")

if __name__ == "__main__":
    print("Starting input simulator...")
    generate_input_data()