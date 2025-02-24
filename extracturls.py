import re

def extract_urls_from_markdown(markdown_file: str, output_file: str):
    # Read the markdown content from the file
    with open(markdown_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Use a regex to extract all text between "](" and ")"
    # This will capture the entire URL (and possibly title) string.
    matches = re.findall(r'\]\((.*?)\)', content)
    
    urls = []
    for match in matches:
        # The match might look like:
        #   "https://hebbarskitchen.com/cuisines/gujarat/<https:/hebbarskitchen.com/badam-burfi-recipe-almond-badam-katli/> "Badam Burfi Recipe | Almond Burfi with Tips & Tricks""
        # Split on whitespace to separate URL from the title.
        parts = match.split()
        if parts:
            # Take the first part and strip out any leading/trailing '<' or '>' characters.
            url = parts[0].strip("<>")
            urls.append(url)
    
    # Append each URL to the output file (one URL per line)
    with open(output_file, "a", encoding="utf-8") as f:
        for url in urls:
            f.write(url + "\n")
    
    print(f"Extracted {len(urls)} URLs and appended them to '{output_file}'.")

if __name__ == "__main__":
    # Replace 'input.md' with your markdown file name,
    # and 'extracted_urls.txt' is the output text file.
    extract_urls_from_markdown("all_cuisines.md", "extracted_urls.txt")
