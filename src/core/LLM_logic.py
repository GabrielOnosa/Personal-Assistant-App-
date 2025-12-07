import openai
from openai import OpenAI
from src.config.config import GEMINI_API_KEY
from qfluentwidgets import *
import src.core.prompts as prompts

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
    clear_conversation()
    conversation[0]["content"] = SYSTEM_PROMPT

#RAG LOGIC HERE



if __name__ == "__main__":
    print(get_response("Hello, how are you?"))

