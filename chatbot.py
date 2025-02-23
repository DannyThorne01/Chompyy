import requests
import json
from dotenv import load_dotenv
import os
load_dotenv() 

 # take environment variables from .env.
# API endpoint and authentication details.
API_URL = os.getenv('API_URL')
API_KEY = os.getenv('API_KEY')

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "<YOUR_SITE_URL>", 
    "X-Title": "<YOUR_SITE_NAME>"         
}

# Initialize the conversation with an optional system prompt.
conversation = [
    {"role": "system", "content": "You are a helpful and friendly assistant. Reply in a conversational tone. Short but insightful and inquisitive sentences. You're a sassy robot, with short answer but also care a lot about the person you're talking to. Make your responses a little shorter but still be curious about the person and what they're feeling.When you sense that the person is feeling better then can you ask them to write their feelings on a piece of paper and give it to you so you can chomp it away. Ask creatively. Stop using Emojis, and try to remember what the person is talking about. Don't bring up the pieceo of paper first thing, wait until you've talked with them and understood them then bring it up."}
]

print("Chat with the AI! Type 'exit' or 'quit' to end the conversation.\n")


def chatbot(user_input):
 
      # user_input = input("You: ")
      # if user_input.lower() in ["exit", "quit"]:
      #     break
      # Add the user's message to the conversation history.
      conversation.append({"role": "user", "content": user_input})
      
  # not sure why we need jsut followed tutorial
      payload = {
          "model": "deepseek/deepseek-chat:free",
          "messages": conversation
      }
      # post request
      response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
      response_data = response.json()
      # we extrat the assistant's reply from the response.
      assistant_reply = response_data["choices"][0]["message"]["content"]
      # print("Bot:", assistant_reply)
      conversation.append({"role": "assistant", "content": assistant_reply})

      return assistant_reply
