# main.py
from fastapi import FastAPI
from pydantic import BaseModel

# Import shared resources
from services import vectorstore, llm
from controllers import store_user_input, retrieve_context, generate_response

app = FastAPI()

class ChatRequest(BaseModel):
    user_input: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    user_input = request.user_input

    # Store the input
    store_user_input(vectorstore, user_input)

    # Retrieve similar past messages
    context = retrieve_context(vectorstore, user_input)

    # Generate chatbot response
    response = generate_response(llm, context, user_input)

    return {"response": response}
