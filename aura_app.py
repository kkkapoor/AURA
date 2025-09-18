import os
import pathway as pw
from dotenv import load_dotenv
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import time
import json

# Load environment variables
load_dotenv()

# Initialize translation models
class TranslationService:
    def __init__(self):
        # Use a single multilingual model for all languages
        print("Loading translation model...")
        try:
            # Use a simpler model that's faster to load
            self.translator = pipeline(
                "translation",
                model="Helsinki-NLP/opus-mt-mul-en",  # Multilingual to English model
                tokenizer="Helsinki-NLP/opus-mt-mul-en"
            )
            # Initialize with a few common languages
            self.supported_languages = ["fr", "hi", "bn", "es", "de", "en"]
            print("Translation service initialized successfully")
        except Exception as e:
            print(f"Error loading translation model: {e}")
            # Fallback to basic translation (for demo purposes)
            self.translator = None
            print("Using fallback translation mechanism")
    
    def detect_language(self, text):
        # Simple language detection based on common words
        # In a production system, use a proper language detection library
        language_markers = {
            "fr": ["le", "la", "les", "je", "tu", "vous", "nous", "et", "ou", "bonjour"],
            "hi": ["है", "में", "और", "का", "की", "के", "को", "से", "पर", "नमस्ते"],
            "bn": ["আমি", "তুমি", "সে", "আমরা", "তারা", "এবং", "কিন্তু", "হ্যালো"],
            "es": ["el", "la", "los", "las", "yo", "tu", "usted", "nosotros", "y", "o", "hola"],
            "de": ["der", "die", "das", "ich", "du", "sie", "wir", "und", "oder", "hallo"]
        }
        
        text_lower = text.lower()
        max_matches = 0
        detected_lang = "en"  # Default to English
        
        for lang, markers in language_markers.items():
            matches = sum(1 for marker in markers if marker in text_lower)
            if matches > max_matches:
                max_matches = matches
                detected_lang = lang
        
        return detected_lang
    
    def translate(self, text, source_lang=None):
        if not text:
            return {"translated_text": "", "source_language": "unknown"}
        
        # Detect language if not provided
        if not source_lang:
            source_lang = self.detect_language(text)
        
        # If it's already English, return as is
        if source_lang == "en":
            return {"translated_text": text, "source_language": "en"}
        
        try:
            # Use the translator if available
            if self.translator:
                translation = self.translator(text)
                translated_text = translation[0]["translation_text"]
            else:
                # Fallback for demo purposes
                translated_text = f"[{source_lang}→en]: {text}"
            
            return {
                "source_text": text,
                "source_lang": source_lang,
                "translated_text": translated_text,
                "target_lang": "en"
            }
        except Exception as e:
            print(f"Translation error: {e}")
            # Return original text if translation fails
            return {
                "source_text": text,
                "source_lang": source_lang,
                "translated_text": f"[Translation Error: {text}]",
                "target_lang": "en"
            }

# Initialize the translation service
translation_service = TranslationService()

# Define Pathway data processing pipeline
class AURAProcessor:
    def __init__(self):
        self.setup_pipeline()
    
    def setup_pipeline(self):
        # Define input schema
        class InputSchema(pw.Schema):
            text: str
            timestamp: float
            session_id: str
        
        # Create input connector for real-time data
        # This could be a file watcher, API endpoint, or other source
        self.input_stream = pw.io.fs.read(
            "./input_data",
            format="json",
            schema=InputSchema,
            mode="streaming"
        )
        
        # Process incoming data
        processed = self.input_stream.select(
            text=pw.this.text,
            timestamp=pw.this.timestamp,
            session_id=pw.this.session_id,
        )
        
        # Apply translation using Python UDF
        translated = processed.select(
            original_text=pw.this.text,
            timestamp=pw.this.timestamp,
            session_id=pw.this.session_id,
            translation=pw.apply(self._translate_text, pw.this.text)
        )
        
        # Output results to a file for the UI to consume
        pw.io.jsonlines.write(translated, "./output_data/translations.jsonl")
    
    def _translate_text(self, text):
        # Call the translation service
        result = translation_service.translate(text)
        return json.dumps(result)
    
    def run(self):
        # Run the pipeline
        pw.run()

# Main application entry point
if __name__ == "__main__":
    # Create input/output directories if they don't exist
    os.makedirs("./input_data", exist_ok=True)
    os.makedirs("./output_data", exist_ok=True)
    
    # Initialize and run the AURA processor
    processor = AURAProcessor()
    processor.run()