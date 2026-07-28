import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
google_api = os.getenv("GOOGLE_API_KEY")
gemini_api = os.getenv("GEMINI_API_KEY")
print(f"GOOGLE_API_KEY starts with: {google_api[:10] if google_api else 'None'}")
print(f"GEMINI_API_KEY starts with: {gemini_api[:10] if gemini_api else 'None'}")

# Initialize client explicitly with the GEMINI_API_KEY to see if that works
try:
    print("\nInitializing client with GEMINI_API_KEY explicitly...")
    client = genai.Client(api_key=gemini_api)
    print("Testing listing models...")
    for model in client.models.list():
        print(f"Model Name: {model.name}")
except Exception as e:
    print(f"Error occurred: {e}")
