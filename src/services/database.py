import sqlite3
from datetime import datetime

#m-am razgandit, nu mai implementez asta inca pentru IOM, dar pastrez codul aici pentru viitor


class ChatHistoryDatabase:
    def __init__(self, db_path='chat_history.db'):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES chat_sessions(id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        conn.close()

    def create_session(self, session_name: str = None) -> int:
        """Create a new chat session and return its ID"""
        if session_name is None:
            session_name = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('INSERT INTO chat_sessions (session_name) VALUES (?)', (session_name,))
        session_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return session_id
    
    def save_message(self, session_id: int, role: str, content: str):
        """Save a single message to a session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO chat_messages (session_id, role, content)
            VALUES (?, ?, ?)
        ''', (session_id, role, content))
        
        # Update session's updated_at timestamp
        cursor.execute('''
            UPDATE chat_sessions SET updated_at = CURRENT_TIMESTAMP WHERE id = ?
        ''', (session_id,))
        
        conn.commit()
        conn.close()

    def save_conversation(self, session_id: int, conversation: list):
        """Save an entire conversation (list of dicts with role and content)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for msg in conversation:
            if msg["role"] != "system":  # Skip system prompts
                cursor.execute('''
                    INSERT INTO chat_messages (session_id, role, content)
                    VALUES (?, ?, ?)
                ''', (session_id, msg["role"], msg["content"]))
        
        cursor.execute('''
            UPDATE chat_sessions SET updated_at = CURRENT_TIMESTAMP WHERE id = ?
        ''', (session_id,))
        
        conn.commit()
        conn.close()

    def load_conversation(self, session_id: int) -> list:
        """Load a conversation from a session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT role, content FROM chat_messages 
            WHERE session_id = ? 
            ORDER BY created_at ASC
        ''', (session_id,))
        
        messages = [{"role": row[0], "content": row[1]} for row in cursor.fetchall()]
        conn.close()
        
        return messages
    
    def get_all_sessions(self) -> list:
        """Get all chat sessions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, session_name, created_at, updated_at 
            FROM chat_sessions 
            ORDER BY updated_at DESC
        ''')
        
        sessions = [
            {"id": row[0], "name": row[1], "created": row[2], "updated": row[3]}
            for row in cursor.fetchall()
        ]
        conn.close()
        
        return sessions
    
    def delete_session(self, session_id: int):
        """Delete a chat session and all its messages"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM chat_sessions WHERE id = ?', (session_id,))
        
        conn.commit()
        conn.close()