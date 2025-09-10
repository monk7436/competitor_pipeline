import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
import json
import os
import time
import random
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

ua = UserAgent()

# Create necessary directories
os.makedirs("raw", exist_ok=True)
os.makedirs("out", exist_ok=True)

def search_domain(query):
    url = f"https://serpapi.com/search.json?q={query}&engine=google&api_key={SEARCH_API_KEY}"
    response = requests.get(url)
    results = response.json().get("organic_results", [])
    domains = set()
    for r in results:
        link = r.get("link")
        if link:
            domain = link.split("/")[2]
            domains.add(domain)
    return list(domains)[:10]

def fetch_page(url, filename):
    try:
        headers = {'User-Agent': ua.random}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            path = os.path.join("raw", filename)
            with open(path, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"Saved {filename}")
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")

def extract_info(html_content):
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

Return ONLY valid JSON.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.3
        )
        text_output = response['choices'][0]['message']['content']
        return json.loads(text_output)
    except Exception as e:
        print("Error in OpenAI API or parsing:", e)
        return {}

def create_brief(df):
    top10 = df.head(10)
    lines = []
    lines.append("# Saturday Brief\n")
    lines.append("## Top 10 Competitors\n")
    for idx, row in top10.iterrows():
        lines.append(f"{idx+1}. **{row['company']}** - {row['one_line']} (Evidence: {row['evidence_urls']})")
    lines.append("\n## 3 Things to Copy\n")
    lines.append("1. Example Feature A - [Link](https://example.com/feature)")
    lines.append("2. Simple Pricing Plan - [Link](https://example.com/pricing)")
    lines.append("3. Clear USP - [Link](https://example.com/usp)")
    lines.append("\n## 3 Things to Avoid\n")
    lines.append("1. Overcomplicated UI - [Link](https://example.com/ui)")
    lines.append("2. Expensive Plans - [Link](https://example.com/pricing)")
    lines.append("3. Lack of Support - [Link](https://example.com/support)")
    
    with open("out/brief.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Brief saved to out/brief.md")

def main():
    query = input("Enter domain topic: ")
    print(f"Searching for competitors for: {query}")
    competitors = search_domain(query)
    print(f"Found {len(competitors)} competitors.")

    # Scrape pages
    for domain in competitors:
        print(f"\nProcessing {domain}")
        base_url = f"https://{domain}"
        pages = {
            f"{domain}_home.html": base_url,
            f"{domain}_pricing.html": base_url + "/pricing",
            f"{domain}_features.html": base_url + "/features",
            f"{domain}_about.html": base_url + "/about"
        }
        for filename, url in pages.items():
            fetch_page(url, filename)
            time.sleep(random.uniform(1, 3))

    # Normalize data
    rows = []
    for domain in competitors:
        filename = f"raw/{domain}_home.html"
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                html_content = f.read()
            info = extract_info(html_content)
            if info:
                rows.append(info)
    
    if rows:
        df = pd.DataFrame(rows)
        df.to_csv("out/competitors.csv", index=False)
        print("\nSaved competitors.csv")
        create_brief(df)
    else:
        print("No data extracted.")

if __name__ == "__main__":
    main()
