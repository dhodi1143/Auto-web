import os
import requests
import google.generativeai as genai

def run_automation():
    # 1. Setup API Keys from your GitHub Secrets
    gemini_key = os.getenv("GEMINI_API_KEY")
    gumroad_token = os.getenv("GUMROAD_TOKEN")
    
    if not gemini_key or not gumroad_token:
        print("Error: Missing GEMINI_API_KEY or GUMROAD_TOKEN in Secrets.")
        return

    # 2. Generate the Content
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('models/gemini-1.5-flash')

    try:
        prompt = "Provide 3 viral tech niches for today with a catchy title and 1-sentence summary for each."
        response = model.generate_content(prompt)
        report_content = response.text

        # 3. Create the Product on Gumroad
        # This sends your AI research directly to your store
        url = "https://api.gumroad.com/v2/products"
        
        # Use a dynamic name based on today's date
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')
        
        payload = {
            "name": f"Daily Viral Tech Report ({today})",
            "price": "0",  # Set to "0" for free or e.g. "100" for $1.00
            "description": report_content,
            "summary": "Daily AI-generated viral tech niche research.",
            "published": "true"
        }
        
        headers = {
            "Authorization": f"Bearer {gumroad_token}"
        }

        res = requests.post(url, headers=headers, data=payload)

        if res.status_code == 201 or res.status_code == 200:
            print("Successfully created product on Gumroad!")
        else:
            print(f"Gumroad API Error: {res.status_code}")
            print(res.text)

    except Exception as e:
        print(f"Automation failed: {e}")

if __name__ == "__main__":
    run_automation()
    
    
