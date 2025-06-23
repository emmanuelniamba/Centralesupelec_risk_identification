#after the first step of preprocessing of llamaparse
from transformers import AutoTokenizer
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
access_token = os.getenv("HUGGING_FACE_API_KEY")  # Get the Hugging Face access token from environment variables
model_id="meta-llama/Llama-4-scout-17B-16E-Instruct" # Specify the model ID for Llama 4 Scout
tokenizer=AutoTokenizer.from_pretrained(model_id,token=access_token) # Load the tokenizer for the specified model with long context support

