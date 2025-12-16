
import openai
from openai import OpenAI
from src.config.config import GEMINI_API_KEY, PINECONE_API_KEY
from qfluentwidgets import *
import src.core.prompts as prompts
from pinecone import Pinecone
from langchain_google_vertexai import VertexAIEmbeddings

client = OpenAI(api_key = GEMINI_API_KEY,
                       base_url="https://generativelanguage.googleapis.com/v1beta/openai/")


SYSTEM_PROMPT = ''


personalities = ['Classic GPT', 'Chill', 'Snarky', 'Strict', 'Comedian']

class MyConfigItem(QConfig):
    change_personality = OptionsConfigItem('SettingsPage', 'ChangePersonality', 'Classic GPT', OptionsValidator(personalities))
    theme_mode = OptionsConfigItem('SettingsPage', 'ThemeMode', 'Dark', OptionsValidator(['Light', 'Dark']))
    temperature = RangeConfigItem('SettingsPage', 'Temperature', 1000, RangeValidator(0, 1800))
    top_p = RangeConfigItem('SettingsPage', 'Temperature', 900, RangeValidator(100, 1000))
    
options = MyConfigItem()
conversation = [{"role": "system", "content": SYSTEM_PROMPT}]

def clear_conversation():
    """Clear the conversation history"""
    global conversation
    conversation = [{"role": "system", "content": SYSTEM_PROMPT}]

def get_response(message, options = options):
    #conversation.append({"role": "user", "content": message})

    rag_context = ''

    if len(message) > 5 and check_if_rag_needed(message):
        rag_context = RAG_retrieval(message)

    if rag_context != '':
        full_mesage = (f"Use the following context to answer the question accurately:\n{rag_context}\nQuestion: {message}")    
        conversation.append({"role": "user", "content": full_mesage})
    else:
        conversation.append({"role": "user", "content": message})
    try:
        print(f"request has the following temperature: {float(options.temperature.value/1000)}")
        response = client.chat.completions.create(
            model = 'gemini-2.5-flash',
            messages = conversation,
            max_completion_tokens= 16384,
            temperature= float(options.temperature.value / 1000),
            top_p = float(options.top_p.value / 1000))
    except openai.RateLimitError:
        return "Sorry, you have reached your API quota. Please try again later."
    except openai.APIConnectionError:
        return "No internet connection. Please check your connection and try again."
    except:
        return "An error occurred while processing your request. Please try again."
    print(response)    
    conversation.append({"role": "assistant", "content": response.choices[0].message.content})

    return response.choices[0].message.content

def change_personality(value):
    global SYSTEM_PROMPT
    if value == 'Chill Buddy':
        SYSTEM_PROMPT = prompts.SYSTEM_PROMPT_CHILL_BUDDY
    elif value == 'Snarky':
        SYSTEM_PROMPT = prompts.SYSTEM_PROMPT_SNARKY
    elif value == 'Strict Librarian':
        SYSTEM_PROMPT = prompts.SYSTEM_PROMPT_STRICT_LIBRARIAN
    elif value == 'Comedian':
        SYSTEM_PROMPT = prompts.SYSTEM_PROMPT_COMEDIAN
    else:
        SYSTEM_PROMPT = prompts.SYSTEM_PROMPT_CLASSIC_GPT
    conversation[0]["content"] = SYSTEM_PROMPT

#RAG LOGIC HERE
def check_if_rag_needed(user_input):
    router_prompt = prompts.RAG_PROMPT
    message = [{"role": "system", "content": router_prompt},
              {"role": "user", "content": user_input}]
    response = client.chat.completions.create(
            model = 'gemini-2.5-flash',
            messages = message,
            temperature= 0.1,
            max_completion_tokens= 500)
    
    print(f"mesaj = {response.choices[0].message.content}")
    decision = response.choices[0].message.content.strip().upper()
    print(decision)
    # DA sau NU
    return decision == "DA"

def RAG_retrieval(user_input):
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index('iom-rag-index')
    print("RAG retrieval initiated.")
    embedding_model = VertexAIEmbeddings(
        model_name="text-embedding-004")
    vector = embedding_model.embed_query(user_input)
    results = index.query(vector = vector, top_k=3, include_metadata=True)
    context_text = " "
    print(results)
    print(" ")
    print("")
    for match in results['matches']:
        text = match['metadata'].get('text', '')
        print(text)
        context_text +=f"---\n{text}\n"
    return context_text

if __name__ == "__main__":
    print(get_response("Hello, how are you?"))

