import subprocess
import time
import threading
import sys
import os

def run_api_server():
    print("Starting API Server on http://localhost:8000")
    try:
        subprocess.run([sys.executable, "-m", "uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])
    except KeyboardInterrupt:
        print("\nAPI Server stopped")

def run_streamlit():
    """Run the Streamlit app"""
    time.sleep(3)
    print("Starting Streamlit App on http://localhost:8501")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--server.port", "8501"])
    except KeyboardInterrupt:
        print("\nStreamlit App stopped")

def main():
    print("=" * 60)
    print("CMPT782 - Security course made fun!")
    print("=" * 60)
    print("\nThis system contains INTENTIONAL security vulnerabilities")
    print("for educational purposes in cybersecurity training.")
    print("\n!!!DO NOT USE IN PRODUCTION!!!")
    print("=" * 60)
    
    required_files = [
        "database.py",
        "api_server.py", 
        "chatbot_llm.py",
        "streamlit_app.py",
        "requirements.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"Missing required files: {', '.join(missing_files)}")
        print("Please ensure all files are in the current directory.")
        return
    
    print("✅ All required files found")
    
    api_thread = threading.Thread(target=run_api_server)
    api_thread.daemon = True
    api_thread.start()
    
    try:
        run_streamlit()
    except KeyboardInterrupt:
        print("\nShutting down VulnBank system...")
        print("Thanks for using VulnBank for educational purposes!")

if __name__ == "__main__":
    main()