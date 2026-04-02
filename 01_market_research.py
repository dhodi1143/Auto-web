import google.generativeai as genai
import os

# Setup API Key from GitHub Secrets
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def generate_content(prompt):
    try:
        # Using the specific 'models/' prefix to resolve the 404 error
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error with primary model: {e}")
        # Fallback to the stable 1.0 version if 1.5 is unrecognized
        print("Attempting fallback to gemini-1.0-pro...")
        model = genai.GenerativeModel('models/gemini-1.0-pro')
        response = model.generate_content(prompt)
        return response.text

# Your existing logic below...
