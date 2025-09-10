import pandas as pd

def create_brief(csv_file="out/competitors.csv"):
    df = pd.read_csv(csv_file)
    top10 = df.head(10)
    
    with open("out/brief.md", "w") as f:
        f.write("# Saturday Brief\n\n")
        
        f.write("## Top 10 Competitors\n\n")
        for idx, row in top10.iterrows():
            f.write(f"{idx+1}. **{row['company']}** - {row['one_line']} (Evidence: {row['evidence_urls']})\n")

        f.write("\n## 3 Things to Copy\n\n")
        f.write("1. Example Feature A - [Link](https://example.com/feature)\n")
        f.write("2. Simple Pricing Plan - [Link](https://example.com/pricing)\n")
        f.write("3. Clear USP - [Link](https://example.com/usp)\n")

        f.write("\n## 3 Things to Avoid\n\n")
        f.write("1. Overcomplicated UI - [Link](https://example.com/ui)\n")
        f.write("2. Expensive Plans - [Link](https://example.com/pricing)\n")
        f.write("3. Lack of Support - [Link](https://example.com/support)\n")

    print("Brief generated at out/brief.md")

if __name__ == "__main__":
    create_brief()
