import os
import subprocess
import time
import signal
import sys

def print_banner():
    """Print AURA banner"""
    print("\n" + "="*60)
    print("  AURA - Augmented Universal Real-time Assistant")
    print("  Real-time multilingual translation system")
    print("="*60 + "\n")

def create_directories():
    """Create necessary directories"""
    directories = ["./input_data", "./output_data", "./enhanced_output", "./knowledge_base"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def start_processes():
    """Start all AURA processes"""
    processes = []
    
    try:
        # Start the main AURA app (Pathway pipeline)
        print("\n📊 Starting AURA Pathway pipeline...")
        aura_process = subprocess.Popen(["python", "aura_app.py"])
        processes.append(("AURA Pipeline", aura_process))
        time.sleep(2)  # Give it time to initialize
        
        # Start the RAG processor
        print("🧠 Starting RAG processor...")
        rag_process = subprocess.Popen(["python", "rag_processor.py"])
        processes.append(("RAG Processor", rag_process))
        time.sleep(2)  # Give it time to initialize
        
        # Start the Streamlit UI
        print("🖥️ Starting Streamlit UI...")
        ui_process = subprocess.Popen(["streamlit", "run", "ui.py"])
        processes.append(("Streamlit UI", ui_process))
        
        print("\n✅ AURA system is now running!")
        print("🌐 Access the UI at: http://localhost:8501")
        print("\nPress Ctrl+C to stop all processes\n")
        
        # Keep the script running until interrupted
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping AURA system...")
        
        # Terminate all processes
        for name, process in processes:
            print(f"Stopping {name}...")
            process.terminate()
            process.wait()
        
        print("✓ All processes stopped")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        
        # Terminate all processes on error
        for name, process in processes:
            process.terminate()
            process.wait()
        
        return 1
    
    return 0

if __name__ == "__main__":
    print_banner()
    create_directories()
    sys.exit(start_processes())