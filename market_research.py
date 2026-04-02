import os
import google.generativeai as genai

def run_research():
    # 1. Configuration - Pulls from GitHub Secrets
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("Error: GEMINI_API_KEY is missing from GitHub Secrets.")
        return
    
    # Configure the SDK
    genai.configure(api_key=api_key)
    
    # 2. Model Setup
    # Using 'models/' prefix is the fix for the 'Model Not Found' error
    try:
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        # 3. Execution
        prompt = "Identify 3 viral tech niches for a blog today. Provide a title and a 1-sentence summary for each."
        response = model.generate_content(prompt)
        
        # Save results so your website/blog can find the content
        with open("research_results.txt", "w") as f:
            f.write(response.text)
            
        print("--- Research Results ---")
        print(response.text)
        print("------------------------")
        print("Research completed and saved to research_results.txt")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_research()
    
