import re

def clean_recipe_urls(input_markdown: str, output_markdown: str):
    """
    Cleans the recipe URLs by removing links that end with '/#comments' or '/#respond'
    and saves them in the required markdown format.

    Parameters:
        input_markdown (str): Path to the input markdown file.
        output_markdown (str): Path to save the cleaned URLs as a markdown file.
    """

    # Define regex pattern to filter unwanted URLs
    unwanted_patterns = [r"/#comments$", r"/#respond$"]

    # Read input markdown file
    with open(input_markdown, "r", encoding="utf-8") as f:
        lines = f.readlines()

    cleaned_urls = []
    for line in lines:
        # Extract the actual URL (ignoring markdown formatting)
        url_match = re.search(r"https?://[^\s)]+", line)  # Avoid trailing markdown )
        if url_match:
            url = url_match.group(0)
            # Ignore URLs ending with unwanted patterns
            if not any(re.search(pattern, url) for pattern in unwanted_patterns):
                cleaned_urls.append(url)

    # Format the cleaned URLs into the required markdown format
    formatted_urls = []
    for url in cleaned_urls:
        parts = url.split("/")
        if len(parts) > 4:  # Ensure there are enough parts in the URL
            cuisine_part = "/".join(parts[:5]) + "/"  # Extract cuisine URL
            recipe_part = f"<{url}>"  # Wrap the recipe URL in <>
            formatted_urls.append(f"{cuisine_part}{recipe_part}")

    # Save cleaned and formatted URLs to a new markdown file
    with open(output_markdown, "w", encoding="utf-8") as f:
        f.writelines("\n".join(formatted_urls) + "\n")

    print(f"Cleaned and formatted URLs saved to: {output_markdown}")

# Example usage
input_markdown = "all_recipe_urls.md"  # Replace with your input markdown file
output_markdown = "cleaned_recipe_urls.md"  # Output markdown file

clean_recipe_urls(input_markdown, output_markdown)
