from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# Relative import, kyunki hum backend folder ke andar hain
from . import chatbot_logic as bot

# FastAPI app banana
app = FastAPI(
    title="Gita-Chatbot API",
    description="An API to get spiritual guidance from the Bhagavad Gita.",
    version="1.0.0"
)

# Yeh Pydantic model data ko validate karta hai
class Query(BaseModel):
    text: str

@app.on_event("startup")
async def startup_event():
    """Server shuru hone par models ko load karta hai."""
    print("🚀 API Server starting up...")
    bot.load_models()
    print("✅ Models loaded, API is ready.")

@app.post("/ask")
async def ask_question(query: Query):
    """
    Yeh mukhya endpoint hai jo user ka sawaal leta hai
    aur streaming response bhejta hai.
    """
    response_generator = bot.generate_answer(query.text)
    return StreamingResponse(response_generator, media_type="text/plain")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Gita-Chatbot API. Please use the /ask endpoint."}

