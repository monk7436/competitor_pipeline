import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def extract_info(html_content):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GEMINI_API_KEY}"
    }
    
    prompt = f"""
You are given HTML content from a competitor's website. Extract the following fields as JSON:
- company
- one_line
- pricing_model
- plans
- top_features
- target_segment
- geography
- notable_clients
- usp
- evidence_urls

HTML content:
\"\"\"{html_content}\"\"\"

Return only valid JSON.
"""

    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "maxOutputTokens": 1000,
            "temperature": 0.3
        }
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        result = response.json()
        try:
            text_output = result['candidates'][0]['content']['parts'][0]['text']
            return json.loads(text_output)
        except Exception as e:
            print("Error parsing response:", e)
            return {}
    else:
        print(f"Gemini API error {response.status_code}: {response.text}")
        return {}

if __name__ == "__main__":
    with open("raw/example.com_home.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    info = extract_info(html_content)
    print(json.dumps(info, indent=2))
