import requests
import json

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": "Bearer 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",
    "Content-Type": "application/json",
  },
  data=json.dumps({
    "model": "deepseek/deepseek-chat-v3.1:free",
    "messages": [
      {
        "role": "user",
        "content": "What is the meaning of life?"
      }
    ],
    
  })
)


data = response.json()

# Extract the assistant's reply
reply = data["choices"][0]["message"]["content"]

print("Assistant:", reply)