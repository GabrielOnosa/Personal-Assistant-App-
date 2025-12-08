
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from src.config.config import PINECONE_API_KEY

def ingest(pdf_path):
    INDEX_NAME = "iom-rag-index" 
    
    loader = PyPDFLoader(pdf_path)
    raw_docs = loader.load()
    print(raw_docs)
    print(f"Loaded {len(raw_docs)} pages.")


    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", "?", "!", " ", ""] 
    )
    documents = text_splitter.split_documents(raw_docs)
   
    embeddings = VertexAIEmbeddings(model_name="text-embedding-004", project = 'copper-citron-476316-n0')
    
    PineconeVectorStore.from_documents(
        documents=documents,
        embedding=embeddings,
        index_name=INDEX_NAME,
        pinecone_api_key=PINECONE_API_KEY
    )
    print("SUCCESS: Knowledge base updated!")

if __name__ == "__main__":
    ingest(r'C:\Users\Onosa\Desktop\Metodologie-burse_2025-2026_12.11.2025_v2.pdf')