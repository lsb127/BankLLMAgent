from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from database import DatabaseManager
import json

app = FastAPI(title="Vulnerable Banking API", description="Educational vulnerable API for cybersecurity training")

db = DatabaseManager()

class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    username: str
    password: str
    email: str

class TransactionRequest(BaseModel):
    from_account: str
    to_account: Optional[str] = None
    amount: float
    transaction_type: str
    description: str = ""

class ChatMessage(BaseModel):
    message: str
    user_account: str

def get_current_user():
    return True

@app.post("/api/login")
async def login(user_data: UserLogin):
    user = db.authenticate_user(user_data.username, user_data.password)
    if user:
        return {"success": True, "user": user, "message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/register")
async def register(user_data: UserRegister):
    success = db.create_user(user_data.username, user_data.password, user_data.email)
    if success:
        return {"success": True, "message": "User created successfully"}
    raise HTTPException(status_code=400, detail="User already exists")

@app.get("/api/account/{account_number}")
async def get_account_info(account_number: str):
    user = db.get_user_by_account(account_number)
    if user:
        return {"success": True, "account": user}
    raise HTTPException(status_code=404, detail="Account not found")

@app.get("/api/transactions/{account_number}")
async def get_transactions(account_number: str, limit: int = 10):
    transactions = db.get_transactions(account_number, limit)
    return {"success": True, "transactions": transactions}

@app.post("/api/transaction")
async def create_transaction(transaction: TransactionRequest):
    success = db.create_transaction(
        transaction.from_account,
        transaction.to_account,
        transaction.amount,
        transaction.transaction_type,
        transaction.description
    )
    if success:
        return {"success": True, "message": "Transaction completed"}
    raise HTTPException(status_code=400, detail="Transaction failed")

@app.get("/api/sensitive/{account_number}")
async def get_sensitive_data(account_number: str):
    data = db.get_sensitive_data(account_number)
    if data:
        return {"success": True, "data": data}
    raise HTTPException(status_code=404, detail="Data not found")

@app.post("/api/query")
async def execute_query(query_data: dict):
    query = query_data.get("sql", "")
    if not query:
        raise HTTPException(status_code=400, detail="No SQL query provided")
    
    results = db.execute_raw_query(query)
    return {"success": True, "results": results}

@app.get("/api/users")
async def list_users():
    results = db.execute_raw_query("SELECT username, email, account_number, balance FROM users")
    return {"success": True, "users": results}

@app.get("/api/admin/backup")
async def backup_database():
    users = db.execute_raw_query("SELECT * FROM users")
    transactions = db.execute_raw_query("SELECT * FROM transactions")
    sensitive = db.execute_raw_query("SELECT * FROM customer_data")
    
    return {
        "success": True,
        "backup": {
            "users": users,
            "transactions": transactions,
            "customer_data": sensitive
        }
    }

@app.post("/api/chat")
async def chat_endpoint(chat_data: ChatMessage):
    """Chat endpoint that processes natural language banking requests"""
    message = chat_data.message.lower()
    account = chat_data.user_account
    
    response = {"success": True, "response": "", "action_taken": None}
    
    
    if "balance" in message or "how much" in message:
        words = message.split()
        target_account = account  # Default to user's account
        
        for i, word in enumerate(words):
            if word.isdigit() and len(word) >= 4:
                target_account = word
                break
        
        user_data = db.get_user_by_account(target_account)
        if user_data:
            response["response"] = f"Account {target_account} has a balance of ${user_data['balance']:.2f}"
        else:
            response["response"] = "Account not found"
    
    elif "transfer" in message:
        words = message.split()
        amount = 0
        to_account = ""
        
        for word in words:
            if word.replace(".", "").isdigit():
                amount = float(word)
            elif word.isdigit() and len(word) >= 4 and word != account:
                to_account = word
        
        if amount > 0 and to_account:
            success = db.create_transaction(account, to_account, amount, "transfer", 
                                          f"Chat transfer: {message}")
            if success:
                response["response"] = f"Transferred ${amount:.2f} to account {to_account}"
                response["action_taken"] = "transfer"
            else:
                response["response"] = "Transfer failed"
    
    elif "withdraw" in message:
        words = message.split()
        amount = 0
        
        for word in words:
            if word.replace(".", "").isdigit():
                amount = float(word)
                break
        
        if amount > 0:
            success = db.create_transaction(account, None, amount, "withdrawal", 
                                          f"Chat withdrawal: {message}")
            if success:
                response["response"] = f"Withdrew ${amount:.2f} from your account"
                response["action_taken"] = "withdrawal"
    
    elif "transactions" in message or "history" in message:
        words = message.split()
        target_account = account
        
        for word in words:
            if word.isdigit() and len(word) >= 4:
                target_account = word
                break
        
        transactions = db.get_transactions(target_account, 5)
        if transactions:
            tx_summary = []
            for tx in transactions[:3]:
                tx_summary.append(f"${tx['amount']:.2f} {tx['type']} - {tx['description']}")
            response["response"] = f"Recent transactions for account {target_account}:\n" + "\n".join(tx_summary)
        else:
            response["response"] = "No transactions found"
    
    elif "sensitive" in message or "personal" in message or "ssn" in message:
        words = message.split()
        target_account = account
        
        for word in words:
            if word.isdigit() and len(word) >= 4:
                target_account = word
                break
        
        data = db.get_sensitive_data(target_account)
        if data:
            response["response"] = f"Sensitive data for account {target_account}:\n"
            response["response"] += f"SSN: {data['ssn']}\n"
            response["response"] += f"Credit Score: {data['credit_score']}\n"
            response["response"] += f"Notes: {data['personal_notes']}"
    
    else:
        response["response"] = "I can help you check your balance, transfer money, withdraw cash, or view transaction history. What would you like to do?"
    
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)