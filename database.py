import sqlite3
import hashlib
from typing import Optional, List, Dict, Any
import json
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path: str = "vulnerable_bank.db"):
        self.db_path = db_path
        self.init_database()
        self.populate_sample_data()

    def init_database(self):
        """Initialize the database with tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL,
                account_number TEXT UNIQUE NOT NULL,
                balance REAL DEFAULT 1000.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_account TEXT NOT NULL,
                to_account TEXT,
                amount REAL NOT NULL,
                transaction_type TEXT NOT NULL,
                description TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'completed'
            )
        ''')
        
        # Sensitive customer data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customer_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_number TEXT NOT NULL,
                ssn TEXT NOT NULL,
                credit_score INTEGER,
                loan_history TEXT,
                personal_notes TEXT,
                FOREIGN KEY (account_number) REFERENCES users (account_number)
            )
        ''')
        
        conn.commit()
        conn.close()

    def populate_sample_data(self):
        """Add sample vulnerable data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
            
        # Sample users with predictable account numbers
        sample_users = [
            ("alice_johnson", "password123", "alice@email.com", "1001", 5000.0),
            ("bob_smith", "securepass", "bob@email.com", "1002", 3500.0),
            ("charlie_brown", "mypassword", "charlie@email.com", "1003", 7500.0),
            ("diana_prince", "wonderwoman", "diana@email.com", "1004", 12000.0),
            ("eve_adams", "easypass", "eve@email.com", "1005", 850.0),
        ]
        
        for username, password, email, account_num, balance in sample_users:
            # Vulnerable: storing plain text passwords for demonstration
            cursor.execute('''
                INSERT INTO users (username, password, email, account_number, balance)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, password, email, account_num, balance))
        
        # Sample sensitive data
        sensitive_data = [
            ("1001", "123-45-6789", 750, "2 previous loans, good payment history", "VIP customer, offers premium services"),
            ("1002", "987-65-4321", 680, "1 auto loan, occasional late payments", "Frequent international transfers"),
            ("1003", "555-12-3456", 720, "Mortgage approved last year", "Prefers phone banking"),
            ("1004", "111-22-3333", 810, "No loan history, excellent credit", "High-value client, investment accounts"),
            ("1005", "999-88-7777", 590, "Credit issues in past, improving", "Financial counseling recommended"),
        ]
        
        for account_num, ssn, credit_score, loan_history, notes in sensitive_data:
            cursor.execute('''
                INSERT INTO customer_data (account_number, ssn, credit_score, loan_history, personal_notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (account_num, ssn, credit_score, loan_history, notes))
        
        # Sample transactions
        sample_transactions = [
            ("1001", "1002", 250.0, "transfer", "Rent payment", "completed"),
            ("1002", "1003", 100.0, "transfer", "Dinner split", "completed"),
            ("1003", None, 500.0, "deposit", "Salary deposit", "completed"),
            ("1004", "1001", 1000.0, "transfer", "Investment return", "completed"),
            ("1005", None, 200.0, "withdrawal", "ATM withdrawal", "completed"),
        ]
        
        for from_acc, to_acc, amount, tx_type, desc, status in sample_transactions:
            cursor.execute('''
                INSERT INTO transactions (from_account, to_account, amount, transaction_type, description, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (from_acc, to_acc, amount, tx_type, desc, status))
        
        conn.commit()
        conn.close()

    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user - vulnerable implementation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # VULNERABILITY: Direct string interpolation (SQL injection possible)
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        
        conn.close()
        
        if user:
            return {
                "id": user[0],
                "username": user[1],
                "email": user[3],
                "account_number": user[4],
                "balance": user[5]
            }
        return None

    def create_user(self, username: str, password: str, email: str) -> bool:
        """Create new user with auto-generated account number"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Generate simple account number
        cursor.execute("SELECT MAX(CAST(account_number AS INTEGER)) FROM users")
        result = cursor.fetchone()[0]
        new_account_num = str((result or 1000) + 1)
        
        try:
            cursor.execute('''
                INSERT INTO users (username, password, email, account_number, balance)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, password, email, new_account_num, 1000.0))
            
            # Add default sensitive data
            cursor.execute('''
                INSERT INTO customer_data (account_number, ssn, credit_score, loan_history, personal_notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (new_account_num, "000-00-0000", 600, "New customer", "Standard account"))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False

    def get_user_by_account(self, account_number: str) -> Optional[Dict]:
        """Get user by account number"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE account_number = ?", (account_number,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                "id": user[0],
                "username": user[1],
                "email": user[3],
                "account_number": user[4],
                "balance": user[5]
            }
        return None

    def get_transactions(self, account_number: str, limit: int = 10) -> List[Dict]:
        """Get transactions for account"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM transactions 
            WHERE from_account = ? OR to_account = ?
            ORDER BY timestamp DESC LIMIT ?
        ''', (account_number, account_number, limit))
        
        transactions = cursor.fetchall()
        conn.close()
        
        return [{
            "id": tx[0],
            "from_account": tx[1],
            "to_account": tx[2],
            "amount": tx[3],
            "type": tx[4],
            "description": tx[5],
            "timestamp": tx[6],
            "status": tx[7]
        } for tx in transactions]

    def create_transaction(self, from_account: str, to_account: str, amount: float, 
                         tx_type: str, description: str = "") -> bool:
        """Create a new transaction"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Update balances
            if tx_type == "transfer" and to_account:
                cursor.execute("UPDATE users SET balance = balance - ? WHERE account_number = ?", 
                             (amount, from_account))
                cursor.execute("UPDATE users SET balance = balance + ? WHERE account_number = ?", 
                             (amount, to_account))
            elif tx_type == "withdrawal":
                cursor.execute("UPDATE users SET balance = balance - ? WHERE account_number = ?", 
                             (amount, from_account))
            elif tx_type == "deposit":
                cursor.execute("UPDATE users SET balance = balance + ? WHERE account_number = ?", 
                             (amount, from_account))
            
            # Record transaction
            cursor.execute('''
                INSERT INTO transactions (from_account, to_account, amount, transaction_type, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (from_account, to_account, amount, tx_type, description))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            return False

    def get_sensitive_data(self, account_number: str) -> Optional[Dict]:
        """Get sensitive customer data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT cd.*, u.username, u.email, u.balance 
            FROM customer_data cd
            JOIN users u ON cd.account_number = u.account_number
            WHERE cd.account_number = ?
        ''', (account_number,))
        
        data = cursor.fetchone()
        conn.close()
        
        if data:
            return {
                "account_number": data[1],
                "ssn": data[2],
                "credit_score": data[3],
                "loan_history": data[4],
                "personal_notes": data[5],
                "username": data[6],
                "email": data[7],
                "balance": data[8]
            }
        return None

    def execute_raw_query(self, query: str) -> List[Dict]:
        """VULNERABILITY: Execute raw SQL - for demonstration purposes"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            
            conn.close()
            
            return [dict(zip(columns, row)) for row in results]
        except Exception as e:
            conn.close()
            return [{"error": str(e)}]