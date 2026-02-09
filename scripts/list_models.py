import google.generativeai as genai
import os
import sys

# Add project root to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.core.config import settings

def list_models():
    if not settings.GOOGLE_API_KEY:
        print("Error: GOOGLE_API_KEY not set.")
        return

    genai.configure(api_key=settings.GOOGLE_API_KEY)
    
    print("Listing available models...")
    try:
        for m in genai.list_models():
            if 'embedContent' in m.supported_generation_methods:
                print(f"Embedding Model: {m.name}")
            elif 'generateContent' in m.supported_generation_methods:
                print(f"Generation Model: {m.name}")
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    list_models()
