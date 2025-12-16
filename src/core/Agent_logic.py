import tweepy
import os
from typing import Annotated, Optional
from typing_extensions import TypedDict
import json
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from vertexai.preview.vision_models import ImageGenerationModel
from google.cloud import aiplatform
from src.config.config import X_API_KEY, X_API_KEY_SECRET, X_API_ACCESS_TOKEN, X_API_ACCESS_TOKEN_SECRET

auth = tweepy.OAuth1UserHandler(X_API_KEY, X_API_KEY_SECRET, X_API_ACCESS_TOKEN, X_API_ACCESS_TOKEN_SECRET)
api_v1 = tweepy.API(auth)

client_v2 = tweepy.Client(
    consumer_key=X_API_KEY,
    consumer_secret=X_API_KEY_SECRET,
    access_token=X_API_ACCESS_TOKEN,
    access_token_secret=X_API_ACCESS_TOKEN_SECRET
)

PROJECT_ID = "copper-citron-476316-n0" 
LOCATION = "us-central1"      

aiplatform.init(project=PROJECT_ID, location=LOCATION)

@tool
def generate_image_with_imagen(prompt: str) -> str:

    """
    Generates a high-quality image using Google's Imagen model on Vertex AI.
    Returns the file path of the saved image locally.
    Use this BEFORE asking to post.
    """

    model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
    
    images = model.generate_images(
        prompt=prompt,
        number_of_images=1,
        aspect_ratio="1:1",
    )
    
    file_path = "temp_imagen_image.png"
    images[0].save(file_path)
    print(f"Google Imagen image saved to {file_path}")
    return file_path

@tool
def post_to_twitter(text: str, image_path: Optional[str] = None, client_v2 = client_v2, auth = auth, api_v1 = api_v1):
    """
    Posts a tweet to Twitter (X). 
    Requires text. Optionally takes a file path to an image.
    ONLY use this when the user explicitly CONFIRMS they want to post.
    """
    print("Attempting to post to Twitter...")
    try:
        media_ids = []
        if image_path and os.path.exists(image_path):
             print(f"Uploading media from path: {image_path}")
             media = api_v1.media_upload(filename=image_path)
             media_ids.append(media.media_id)
             
        response = client_v2.create_tweet(text=text, media_ids=media_ids if media_ids else None)
        
        return f"Successfully posted tweet! ID: {response.data['id']}"
    except Exception as e:

        if hasattr(e, 'response') and e.response is not None:
            print(f"⬇️ FULL API RESPONSE DETAILS ⬇️")
            try:
                # Pretty print the JSON so it's readable
                error_json = json.loads(e.response.text)
                print(json.dumps(error_json, indent=2))
            except:
                print(e.response.text)
        print(f"Error posting tweet: {e}")
        return f"Error posting tweet: {e}"
    


class State(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatVertexAI(model="gemini-2.5-pro")

tools = [generate_image_with_imagen, post_to_twitter]
llm_with_tools = llm.bind_tools(tools)

sys_prompt = SystemMessage(content="""
You are a social media creative director.
When asked to create content:
1. First, generate a creative text draft for the post.
2. Next, look at your draft and create a highly detailed, visual prompt for an image that perfectly matches the mood. Call the `generate_image_with_imagen` tool with this prompt.
3. STOP and submit your draft text and the generated image path to the human user for review.
4. DO NOT call `post_to_twitter` until the human user explicitly confirms with a "yes" or similar.
Once confirmed, use the `post_to_twitter` tool with BOTH the text draft and the image path you generated previously.
NEVER CALL THE POST TOOL WITHOUT CONFIRMATION.
NEVER give the image path to the user. Just the text draft for review. The image path is for your internal use only. 
When asking to post, ALWAYS Give the tweet's text in QUOTES like this:
                           
Example: 
Here is what I cooked up for you: "Tweet content goes here." Would you like me to post it?
""")

def chatbot(state: State):

    msgs = [sys_prompt] + state["messages"]
    return {"messages": [llm_with_tools.invoke(msgs)]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=tools))

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
#graph_builder.add_edge("chatbot", END)

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

