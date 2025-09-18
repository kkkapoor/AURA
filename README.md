# AURA (Augmented Universal Real-time Assistant)

AURA is a real-time multilingual translation system designed to enhance communication by solving linguistic challenges in real-time. It allows users to speak or type words in their native language and receive instant English translations.

## Features

- Real-time data processing using Pathway
- Support for multiple languages (French, Hindi, Bengali, Spanish, German)
- Simple and intuitive user interface
- Instant translation feedback

## Architecture

AURA uses the following components:

1. **Pathway Pipeline**: For real-time data ingestion and processing
2. **Translation Models**: Pre-trained models for multilingual translation
3. **Streamlit UI**: For user interaction and displaying translations

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd AURA
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the Pathway processing pipeline:
   ```
   python aura_app.py
   ```

2. In a separate terminal, start the Streamlit UI:
   ```
   streamlit run ui.py
   ```

3. (Optional) Run the input simulator to generate test data:
   ```
   python input_simulator.py
   ```

## Usage

1. Open the Streamlit UI in your browser (typically at http://localhost:8501)
2. Select your preferred language from the dropdown menu
3. Type or speak a word or phrase in your native language
4. Receive the English translation in real-time

## Project Structure

- `aura_app.py`: Main application with Pathway pipeline
- `ui.py`: Streamlit-based user interface
- `input_simulator.py`: Tool to generate test data
- `requirements.txt`: Project dependencies
- `input_data/`: Directory for input data files
- `output_data/`: Directory for processed output files

## Future Enhancements

- Add support for more languages
- Implement speech-to-text for voice input
- Enhance language detection accuracy
- Add context-aware translation capabilities using RAG

## License

[MIT License](LICENSE)