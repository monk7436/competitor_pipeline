from search import search_domain
from scrape import fetch_page
from normalize import extract_info
import csv
import os

def main():
    os.makedirs("raw", exist_ok=True)
    os.makedirs("out", exist_ok=True)

    query = input("Enter domain topic: ")
    competitors = search_domain(query)[:10]
    print(f"Found {len(competitors)} competitors.")

    # Scraping pages
    for domain in competitors:
        print(f"Processing {domain}")
        base_url = f"https://{domain}"
        pages = {
            f"{domain}_home.html": base_url,
            f"{domain}_pricing.html": base_url + "/pricing",
            f"{domain}_features.html": base_url + "/features",
            f"{domain}_about.html": base_url + "/about"
        }
        for filename, url in pages.items():
            fetch_page(url, filename)

    # Normalizing data
    rows = []
    for domain in competitors:
        filename = f"raw/{domain}_home.html"
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                html_content = f.read()
            info = extract_info(html_content)
            if info:
                rows.append(info)

    # Write to CSV
    if rows:
        keys = rows[0].keys()
        with open("out/competitors.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(rows)
        print("Data saved to out/competitors.csv")
    else:
        print("No data extracted.")

if __name__ == "__main__":
    main()
