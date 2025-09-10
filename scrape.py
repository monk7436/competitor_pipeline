import requests
from fake_useragent import UserAgent
import time
import random
import os

ua = UserAgent()

SAVE_DIR = "raw/"

def fetch_page(url, filename):
    try:
        headers = {'User-Agent': ua.random}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            os.makedirs(SAVE_DIR, exist_ok=True)
            path = os.path.join(SAVE_DIR, filename)
            with open(path, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"Saved {filename}")
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")

if __name__ == "__main__":
    domain = "example.com"
    urls = {
        f"{domain}_home.html": f"https://{domain}",
        f"{domain}_pricing.html": f"https://{domain}/pricing"
    }
    for filename, url in urls.items():
        fetch_page(url, filename)
        time.sleep(random.uniform(2, 5))
