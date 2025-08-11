
import requests
import json


class LLM:
  def __init__(self, api_key, prompt):
    self.api_key = api_key
    self.prompt = prompt

  def generate_response(self, model="deepseek/deepseek-r1-0528-qwen3-8b:free", temperature=0.2):
     self.model = model
     self.temperature = temperature
     response= requests.post(
      "https://openrouter.ai/api/v1/chat/completions",
      headers={
        "Authorization": f"Bearer {self.api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
        "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
      },
      data=json.dumps({
        "model": self.model,
        "temperature": self.temperature,
        "messages": [
          {
            "role": "user",
            "content": self.prompt
          }
        ]
      })
    )
     return response.json()["choices"][0]["message"]["content"]
   

 
