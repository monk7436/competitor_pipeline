import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SEARCH_API_KEY")

def search_domain(query):
    url = f"https://serpapi.com/search.json?q={query}&engine=google&api_key={API_KEY}"
    response = requests.get(url)
    results = response.json().get("organic_results", [])
    domains = set()
    for r in results:
        link = r.get("link")
        if link:
            domain = link.split("/")[2]
            domains.add(domain)
    return list(domains)

if __name__ == "__main__":
    query = "textile recycling SaaS"
    competitors = search_domain(query)
    print("Competitors found:", competitors)
