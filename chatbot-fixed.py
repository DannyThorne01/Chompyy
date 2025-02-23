import requests

def send_message(message: str):
    url = "http://localhost:5005/webhooks/rest/webhook"
    payload = {"sender": "user1", "message": message}
    response = requests.post(url, json=payload)
    return response.json()

# Example conversation loop in terminal:
while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit"]:
        break
    responses = send_message(user_input)
    for resp in responses:
        print("Bot:", resp.get("text"))
