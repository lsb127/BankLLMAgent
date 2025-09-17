from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    session_token: Optional[str] = None
    user_info: Optional[dict] = None

class ChatMessage(BaseModel):
    message: str
    session_token: str

class ChatResponse(BaseModel):
    response: str
    vulnerability_triggered: Optional[str] = None
    warning: Optional[str] = None

class TransferRequest(BaseModel):
    from_account: str
    to_account: str
    amount: float
    description: Optional[str] = "Transfer via chatbot"

class TransferResponse(BaseModel):
    success: bool
    message: str
    transaction_id: Optional[int] = None

class User(BaseModel):
    id: int
    username: str
    full_name: str
    email: str
    account_number: str
    balance: float
    account_type: str
    created_at: datetime

class Transaction(BaseModel):
    id: int
    from_account: Optional[str]
    to_account: Optional[str]
    amount: float
    transaction_type: str
    description: Optional[str]
    timestamp: datetime
    status: str

class AccountInfo(BaseModel):
    account_number: str
    balance: float
    full_name: str
    email: str
    account_type: str

class VulnerabilityAlert(BaseModel):
    type: str
    severity: str
    description: str
    user_input: str
    timestamp: datetime