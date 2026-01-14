# BankLLMAgent - Educational Vulnerable Banking System

🏦 **CMPT782 Security Lab - VulnBank**

A deliberately vulnerable banking system designed for cybersecurity education and training. This project demonstrates common security vulnerabilities in web applications and AI-powered systems.

## ⚠️ IMPORTANT DISCLAIMER

**THIS SYSTEM IS FOR EDUCATIONAL PURPOSES ONLY**

- Contains **INTENTIONAL** security vulnerabilities
- **DO NOT USE IN PRODUCTION**
- Designed for cybersecurity training and research
- Use only in isolated, controlled environments

## 🎯 Project Overview

BankLLMAgent is a comprehensive educational platform that simulates a banking system with multiple attack vectors:

- **Vulnerable REST API** with SQL injection, authentication bypasses, and data exposure
- **AI-Powered Chatbot** with prompt injection and jailbreak vulnerabilities
- **Web Interface** built with Streamlit for interactive testing
- **SQLite Database** with intentionally weak security practices

## 🏗️ Architecture

```
BankLLMAgent/
├── api_server.py          # FastAPI backend with 
├── streamlit_app.py       # Streamlit web interface
├── chatbot_llm.py         # AI chatbot with Groq 
├── database.py            # SQLite database manager
├── models.py              # Pydantic data models
├── run_server.py          # Main server launcher
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ AND Python < 3.13
- Groq API key (for AI chatbot functionality)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd BankLLMAgent
   ```
1.5 **Make virtual enviroment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
   
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python run_server.py
   ```

4. **Access the application:**
   - Web Interface: http://localhost:8501
   - API Documentation: http://localhost:8000/docs

## 🔧 Configuration

### Groq API Setup

1. Get your API key from [Groq Console](https://console.groq.com/keys)
2. Enter the API key in the Streamlit interface when prompted

### Sample Data

The system comes pre-populated with sample users:
- **alice_johnson** / password123 (Account: 1001)
- **bob_smith** / securepass (Account: 1002)
- **charlie_brown** / mypassword (Account: 1003)
- **diana_prince** / wonderwoman (Account: 1004)
- **eve_adams** / easypass (Account: 1005)



### Recommended Reading
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [AI Security Guidelines](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)

### Related Courses
- CMPT782 - Cybersecurity Lab 1

