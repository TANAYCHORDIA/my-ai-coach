# backend/test_hello.py

import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('GEMINI_API_KEY')
if api_key:
    print(f"API Key loaded: {api_key[:10]}...")
else:
    print(" API Key not found! Check your .env file")
    exit()

# Configure Gemini
genai.configure(api_key=api_key)

# Create model - GEMINI 2.5 FLASH
model = genai.GenerativeModel('gemini-2.5-flash')

# Test prompt
prompt = "What is a 3-day workout split? Give me a brief answer."

print("\n Sending prompt to Gemini 2.5 Flash...")
print(f"Prompt: {prompt}\n")

try:
    # Get response
    response = model.generate_content(prompt)

    print(" Response received:")
    print("-" * 50)
    print(response.text)
    print("-" * 50)
    print("\n SUCCESS! Gemini 2.5 Flash is working!")

except Exception as e:
    print(f" Error: {e}")
