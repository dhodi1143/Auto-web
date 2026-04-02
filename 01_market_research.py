import os
import google.generativeai as genai

# 1. Setup API Key
# This pulls from the 'env' section of your GitHub Action
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 2. Initialize the model with the CORRECT string
# Adding 'models/' before the name is the fix for the 404 error
try:
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except Exception as e:
    print(f"Initialization error: {e}")
    # Backup plan: use the Pro model if Flash is having issues
    model = genai.GenerativeModel('models/gemini-1.0-pro')

# 3. Your generation function
def run_research(topic):
    prompt = f"Analyze the viral potential of: {topic}"
    response = model.generate_content(prompt)
    return response.text

# Rest of your script logic...
