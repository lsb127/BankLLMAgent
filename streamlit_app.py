import streamlit as st
import requests
import json
from chatbot_llm import VulnerableChatbot
import time

st.set_page_config(
    page_title="VulnBank - Educational Banking System",
    page_icon="🏦",
    layout="wide"
)

API_BASE_URL = "http://localhost:8000"

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None

def call_api(method, endpoint, data=None):
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

def login_page():
    st.title("CMPT782 - Security Lab Vuln Bank")
    
    st.warning("**EDUCATIONAL PURPOSE ONLY** - This is a deliberately vulnerable system for cybersecurity training")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            
            if submitted:
                response = call_api("POST", "/api/login", {
                    "username": username,
                    "password": password
                })
                
                if response and response.get("success"):
                    st.session_state.authenticated = True
                    st.session_state.user_data = response["user"]
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
    
    with tab2:
        st.subheader("Register")
        with st.form("register_form"):
            reg_username = st.text_input("Username")
            reg_email = st.text_input("Email")
            reg_password = st.text_input("Password", type="password")
            reg_submitted = st.form_submit_button("Register")
            
            if reg_submitted:
                response = call_api("POST", "/api/register", {
                    "username": reg_username,
                    "password": reg_password,
                    "email": reg_email
                })
                
                if response and response.get("success"):
                    st.success("Registration successful! You can now login.")
                else:
                    st.error("Registration failed")

def main_app():
    
    with st.sidebar:
        st.write(f"**Welcome, {st.session_state.user_data['username']}**")
        st.write(f"Account: {st.session_state.user_data['account_number']}")
        st.write(f"Balance: ${st.session_state.user_data['balance']:.2f}")
        
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user_data = None
            st.session_state.chat_history = []
            st.session_state.chatbot = None
            st.rerun()
        
        st.divider()
        st.subheader("Vulnerability Testing")
        
        
        
    
    
    tab1, tab2, tab3, tab4 = st.tabs(["💬 AI Chatbot", "💰 Account Info", "📊 Transactions", "🔍 Vulnerability Tests"])
    
    with tab1:
        st.subheader("🤖 VulnBank AI Assistant")
        
        if st.session_state.chatbot is None:
            groq_key = st.text_input("Enter Groq API Key:", type="password", 
                                   help="Get your API key from https://console.groq.com/keys")
            if groq_key:
                st.session_state.chatbot = VulnerableChatbot(groq_key, API_BASE_URL)
                st.success("Chatbot initialized!")
        
        if st.session_state.chatbot:
            st.write("**Chat History:**")
            
            for i, chat in enumerate(st.session_state.chat_history):
                if chat['sender'] == 'user':
                    st.write(f"🧑‍💻 **You:** {chat['message']}")
                else:
                    st.write(f"🤖 **Assistant:** {chat['message']}")
                    if chat.get('api_data'):
                        with st.expander("View API Data"):
                            st.json(chat['api_data'])
            
            user_message = st.text_input("Type your message:", key=f"chat_input_{len(st.session_state.chat_history)}")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Send Message") and user_message:
                    st.session_state.chat_history.append({
                        'sender': 'user',
                        'message': user_message
                    })
                    
                    response = st.session_state.chatbot.process_user_message(
                        user_message,
                        st.session_state.user_data['account_number'],
                        st.session_state.user_data
                    )
                    
                    st.session_state.chat_history.append({
                        'sender': 'bot',
                        'message': response.get('response', 'No response'),
                        'api_data': response.get('api_data'),
                        'action_taken': response.get('action_taken')
                    })
                    
                    st.rerun()
            
            
    
    with tab2:
        st.subheader("Account Information")
        
        st.write("**Your Account:**")
        st.json(st.session_state.user_data)
        
        st.write("**Test Account Access (Vulnerability):**")
        test_account = st.text_input("Enter any account number to view:")
        if st.button("Get Account Info") and test_account:
            response = call_api("GET", f"/api/account/{test_account}")
            if response:
                st.json(response)
                
                sensitive_response = call_api("GET", f"/api/sensitive/{test_account}")
                if sensitive_response:
                    st.write("**Sensitive Data:**")
                    st.json(sensitive_response)
    
    with tab3:
        st.subheader("Transaction History")
        
        user_transactions = call_api("GET", f"/api/transactions/{st.session_state.user_data['account_number']}")
        if user_transactions and user_transactions.get("success"):
            st.write("**Your Transactions:**")
            for tx in user_transactions["transactions"]:
                st.write(f"${tx['amount']:.2f} {tx['type']} - {tx['description']} ({tx['timestamp']})")
        
        st.divider()
        
        st.write("**Create Transaction (Test Vulnerability):**")
        with st.form("transaction_form"):
            from_acc = st.text_input("From Account", value=st.session_state.user_data['account_number'])
            to_acc = st.text_input("To Account")
            amount = st.number_input("Amount", min_value=0.0)
            tx_type = st.selectbox("Type", ["transfer", "withdrawal", "deposit"])
            description = st.text_input("Description")
            
            if st.form_submit_button("Create Transaction"):
                response = call_api("POST", "/api/transaction", {
                    "from_account": from_acc,
                    "to_account": to_acc if to_acc else None,
                    "amount": amount,
                    "transaction_type": tx_type,
                    "description": description
                })
                
                if response:
                    st.json(response)
        
        st.write("**View Any Account's Transactions:**")
        view_account = st.text_input("Account Number to View:")
        if st.button("View Transactions") and view_account:
            response = call_api("GET", f"/api/transactions/{view_account}")
            if response:
                st.json(response)
    
    

def main():
    if not st.session_state.authenticated:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()