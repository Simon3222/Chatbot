# ==========================================================
# IMPORT REQUIRED LIBRARIES
# ==========================================================

# Used to access environment variables
import os

# Used to load variables from .env file
from dotenv import load_dotenv

# FastAPI framework for building APIs
from fastapi import FastAPI

# Used to define request body structure
from pydantic import BaseModel

# Groq LLM from LangChain
from langchain_groq import ChatGroq

# Used to create structured prompts
from langchain_core.prompts import ChatPromptTemplate

# MongoDB client
from pymongo import MongoClient

# Used to store timestamps
from datetime import datetime

# Used for SSL certificate verification (important for MongoDB Atlas)
import certifi


# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

# Load .env file variables
load_dotenv()

# Get API keys and MongoDB URI
groq_api_key = os.getenv("GROQ_API_KEY")
mongo_uri = os.getenv("MONGODB_URI")

# Safety checks
if not groq_api_key:
    raise ValueError("GROQ_API_KEY is missing in .env file")

if not mongo_uri:
    raise ValueError("MONGODB_URI is missing in .env file")


# ==========================================================
# INITIALIZE FASTAPI APPLICATION
# ==========================================================

# This is REQUIRED for uvicorn: app:app
app = FastAPI(title="AI Chatbot API 🚀")


# ==========================================================
# CONNECT TO MONGODB
# ==========================================================

# Create MongoDB client (TLS required for Atlas)
client = MongoClient(
    mongo_uri,
    tls=True,
    tlsCAFile=certifi.where()
)

# Access database named "chat"
db = client["chat"]

# Access collection named "user"
collection = db["user"]


# ==========================================================
# DEFINE LLM PROMPT TEMPLATE
# ==========================================================

"""
This template defines:
- System role (AI personality)
- Conversation history
- New user question
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an app developer bot. Answer with respect to creating Python apps."),
        ("placeholder", "{history}"),
        ("user", "{question}")
    ]
)


# ==========================================================
# INITIALIZE GROQ MODEL
# ==========================================================

llm = ChatGroq(
    api_key=groq_api_key,
    model="openai/gpt-oss-20b"
)

# Combine prompt + model into a chain
chain = prompt | llm


# ==========================================================
# REQUEST MODEL (What API expects from user)
# ==========================================================

class ChatRequest(BaseModel):
    user_id: str
    question: str


# ==========================================================
# FUNCTION TO FETCH CHAT HISTORY
# ==========================================================

def get_history(user_id: str):
    """
    Retrieve previous conversation messages
    from MongoDB sorted by timestamp.
    """

    chats = collection.find({"user_id": user_id}).sort("timestamp", 1)

    history = []

    for chat in chats:
        history.append({
            "role": chat["role"],
            "content": chat["message"]
        })

    return history


# ==========================================================
# ROOT ENDPOINT (Health Check)
# ==========================================================

@app.get("/")
def home():
    """
    Simple endpoint to verify server is running.
    """
    return {"message": "Chatbot API is running 🚀"}


# ==========================================================
# CHAT ENDPOINT
# ==========================================================

@app.post("/chat")
def chat(request: ChatRequest):
    """
    Main chatbot endpoint.

    Steps:
    1. Get conversation history
    2. Send history + question to LLM
    3. Save both messages to MongoDB
    4. Return AI response
    """

    # Fetch previous messages
    history = get_history(request.user_id)

    # Send to LLM
    response = chain.invoke({
        "history": history,
        "question": request.question
    })

    answer_text = response.content

    # Save user message
    collection.insert_one({
        "user_id": request.user_id,
        "role": "user",
        "message": request.question,
        "timestamp": datetime.utcnow()
    })

    # Save assistant response
    collection.insert_one({
        "user_id": request.user_id,
        "role": "assistant",
        "message": answer_text,
        "timestamp": datetime.utcnow()
    })

    # Return response
    return {
        "user_id": request.user_id,
        "answer": answer_text
    }