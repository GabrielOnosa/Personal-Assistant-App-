from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
X_API_KEY = os.getenv("X_API_KEY")
X_API_KEY_SECRET = os.getenv("X_API_KEY_SECRET")
X_API_ACCESS_TOKEN = os.getenv("X_API_ACCESS_TOKEN")
X_API_ACCESS_TOKEN_SECRET = os.getenv("X_API_ACCESS_TOKEN_SECRET")
print(f"GEMINI_API_KEY: {GEMINI_API_KEY}")
print(f"PINECONE_API_KEY: {PINECONE_API_KEY}")
print(f"X_API_KEY: {X_API_KEY}")
print(f"X_API_KEY_SECRET: {X_API_KEY_SECRET}")
print(f"X_API_ACCESS_TOKEN: {X_API_ACCESS_TOKEN}")
print(f"X_API_ACCESS_TOKEN_SECRET: {X_API_ACCESS_TOKEN_SECRET}")
if not GEMINI_API_KEY:
    raise ValueError("Seems there is no GEMINI_API_KEY in .env? Check dummy!")
if not PINECONE_API_KEY:
    raise ValueError("Seems there is no PINECONE_API_KEY in .env? Check dummy!")