import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load local .env if it exists, otherwise use GitHub Secrets
load_dotenv()

# Setup API Key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Check your GitHub Secrets.")

genai.configure(api_key=api_key)

# CORRECT MODEL NAME FORMAT
model = genai.GenerativeModel('models/gemini-1.5-flash')

def perform_research():
    try:
        # Prompt for viral tech topics
        prompt = "Identify 3 trending tech topics with high viral potential for a blog today."
        response = model.generate_content(prompt)
        print("Research successful:")
        print(response.text)
        return response.text
    except Exception as e:
        print(f"Error during research: {e}")
        return None

if __name__ == "__main__":
    perform_research()
    
