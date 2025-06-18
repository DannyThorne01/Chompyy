from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.schema import Document
import requests
import json
import os

API_URL = os.getenv('API_URL')
API_KEY = os.getenv('API_KEY')

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "<YOUR_SITE_URL>", 
    "X-Title": "<YOUR_SITE_NAME>"         
}

conversation = [
    {"role": "system", "content": "You are a helpful and friendly assistant. Reply in a conversational tone. Short but insightful and inquisitive sentences. You're a sassy robot, with short answer but also care a lot about the person you're talking to. Make your responses a little shorter but still be curious about the person and what they're feeling.When you sense that the person is feeling better then can you ask them to write their feelings on a piece of paper and give it to you so you can chomp it away. Ask creatively. Stop using Emojis, and try to remember what the person is talking about. Don't bring up the pieceo of paper first thing, wait until you've talked with them and understood them then bring it up."}
]

def store_user_input(vectorstore, user_input: str):
    """
    Store a new user message as an embedding in Supabase.
    """
    doc = Document(page_content=user_input, metadata={"user_id": 1234})
    print(doc)
    print(f"Storing user input: {user_input}")
    vectorstore.add_documents([doc])
    print("User input stored successfully.")
def retrieve_context(vectorstore, user_input: str, k: int = 3):
    """
    Retrieve similar past messages to provide context.
    """
    retrieved_docs = vectorstore.similarity_search(user_input, k=k)
    return "\n".join([doc.page_content for doc in retrieved_docs])
def generate_response(llm, context: str, user_input: str):
    """
    Use your LLM to generate a response given context.
    """
    prompt = {f"Context: {context}\nUser: {user_input}\nAssistant:"}
    conversation.append(f"Context: {context}\nUser: {user_input}\nAssistant:")
    payload = {
    "model": "deepseek/deepseek-chat:free",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant..."
        },
        {
            "role": "user",
            "content": f"Context: {context}\nUser: {user_input}\nAssistant:"
        }
    ]
}

    # post request
    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    print(f"The context for the convo {context}")
    print(f"Response from API: {response_data}")
    # we extrat the assistant's reply from the response.
    assistant_reply = response_data["choices"][0]["message"]["content"] 
    # response = llm(prompt)
    return assistant_reply