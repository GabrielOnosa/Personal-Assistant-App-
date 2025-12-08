from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
print(f"GEMINI_API_KEY: {GEMINI_API_KEY}")
print(f"PINECONE_API_KEY: {PINECONE_API_KEY}")
if not GEMINI_API_KEY:
    raise ValueError("Seems there is no GEMINI_API_KEY in .env? Check dummy!")
if not PINECONE_API_KEY:
    raise ValueError("Seems there is no PINECONE_API_KEY in .env? Check dummy!")