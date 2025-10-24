# check_models.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

print("Attempting to list available models...")

try:
    
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("\nERROR: GOOGLE_API_KEY not found in .env file.")
    else:
        genai.configure(api_key=api_key)
        print("Successfully configured API key.")

        print("\n--- Available Models ---")
        model_found = False
        for m in genai.list_models():
            model_found = True
            
            if 'generateContent' in m.supported_generation_methods:
                print(f"Model Name: {m.name}")
        
        if not model_found:
            print("No models were found for this API key.")

        print("--- End of List ---\n")

except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")