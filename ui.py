import streamlit as st
import json
import os
import time
import uuid
from datetime import datetime
import glob

# Set page configuration
st.set_page_config(
    page_title="AURA - Augmented Universal Real-time Assistant",
    page_icon="🌐",
    layout="wide"
)

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

# App title and description
st.title("🌐 AURA")
st.subheader("Augmented Universal Real-time Assistant")
st.markdown("""
AURA enhances multilingual communication by solving linguistic challenges in real-time.
Speak or type a word in your native language, and AURA will translate it to English instantly.
""")

# Sidebar with language selection
st.sidebar.title("Settings")
selected_language = st.sidebar.selectbox(
    "Select your language",
    ["Auto-detect", "French (Français)", "Hindi (हिन्दी)", "Bengali (বাংলা)", "Spanish (Español)", "German (Deutsch)"]
)

language_code_map = {
    "Auto-detect": None,
    "French (Français)": "fr",
    "Hindi (हिन्दी)": "hi",
    "Bengali (বাংলা)": "bn",
    "Spanish (Español)": "es",
    "German (Deutsch)": "de"
}

selected_lang_code = language_code_map[selected_language]

# Function to write input data
def write_input_data(text, session_id):
    os.makedirs("./input_data", exist_ok=True)
    
    data = {
        "text": text,
        "timestamp": time.time(),
        "session_id": session_id
    }
    
    filename = f"./input_data/input_{int(time.time())}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    
    return filename

# Function to check for output data
def check_for_output(timeout=5, check_interval=0.5):
    start_time = time.time()
    latest_output = None
    
    while time.time() - start_time < timeout:
        # Get list of output files
        output_files = glob.glob("./output_data/*.json")
        
        if output_files:
            # Sort by modification time (newest first)
            latest_file = max(output_files, key=os.path.getmtime)
            
            try:
                with open(latest_file, "r", encoding="utf-8") as f:
                    latest_output = json.load(f)
                break
            except Exception as e:
                st.error(f"Error reading output file: {e}")
        
        time.sleep(check_interval)
    
    return latest_output

# Main input area
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("Input")
    input_text = st.text_area("Enter text in your native language:", height=100)
    
    col_btn1, col_btn2 = st.columns([1, 3])
    with col_btn1:
        submit_button = st.button("Translate", type="primary")
    with col_btn2:
        mic_button = st.button("🎤 Speak (Microphone Input)")

# Process input when button is clicked
if submit_button and input_text:
    # Add to message history
    st.session_state.messages.append({"role": "user", "content": input_text, "time": datetime.now().strftime("%H:%M:%S")})
    
    # Write input to file for Pathway to process
    write_input_data(input_text, st.session_state.session_id)
    
    # Wait for and check output
    with st.spinner("Translating..."):
        output_data = check_for_output()
    
    if output_data:
        # Extract translation from output
        translation_json = json.loads(output_data.get("translation", "{}"))
        translated_text = translation_json.get("translated_text", "Translation not available")
        source_language = translation_json.get("source_language", "unknown")
        
        # Add to message history
        st.session_state.messages.append({
            "role": "assistant", 
            "content": translated_text,
            "source_language": source_language,
            "time": datetime.now().strftime("%H:%M:%S")
        })
    else:
        st.error("No translation received. Please try again.")

# Display translation history
with col2:
    st.subheader("Translation History")
    
    if not st.session_state.messages:
        st.info("No translations yet. Enter text to get started.")
    
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**You ({msg['time']}):**")
            st.markdown(f"> {msg['content']}")
        else:
            source_lang = msg.get("source_language", "unknown")
            lang_name = next((k for k, v in language_code_map.items() if v == source_lang), "Auto-detected")
            
            st.markdown(f"**AURA ({msg['time']}) - {lang_name}:**")
            st.success(msg['content'])
    
    if st.session_state.messages:
        if st.button("Clear History"):
            st.session_state.messages = []
            st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("AURA - Powered by Pathway and LLM technology")