# import asyncio
# import re
# from crawl4ai import *

# async def main():
#     async with AsyncWebCrawler() as crawler:
#         result = await crawler.arun(
#             url="https://hebbarskitchen.com/instant-rava-dosa-recipe-suji-ka-dosa/",
#         )
#         markdown_content = result.markdown

#         ignore_headings = [
#         "#### SUBSCRIBE TO OUR RECIPES",
#         "#### POPULAR RECIPES",
#         "#### POPULAR CATEGORIES",
#         "#### Stay in Touch",
#         "#### Popular",
#         "#### Search Recipes",
#         "##  Rate This Recipe",
#         "##  Recipe Ratings without Comment",
#         "#### BROWSE BY CATEGORIES",
#         "#### STAY CONNECTED",
#         "#### Related Recipes",
#         "#### OUR OTHER LANGUAGES",
#         "#### Must Read:",
#         "#### What's New"
#         ]


#         # Extract only sections that start with ## or ###
#         matches = re.findall(r"(##+ .+?)(?=\n##|\n\Z)", markdown_content, re.DOTALL)

#         cleaned_content = []
#         for section in matches:
#             # Check if the section contains an ignored heading
#             if any(heading in section for heading in ignore_headings):
#                 continue  # Skip unwanted sections

#             # Remove `####` headings that are empty (i.e., no text after them)
#             section = re.sub(r"#### .*\n\s*\n", "", section)
            
#             # Remove Markdown links
#             cleaned_text = re.sub(r"\[.*?\]\(.*?\)", "", section)  
#             cleaned_content.append(cleaned_text.strip())

#         # Join all extracted content
#         final_markdown = "\n\n".join(cleaned_content)

#         # Save to a new markdown file
#         with open("final_filtered_recipe.md", "w", encoding="utf-8") as f:
#             f.write(final_markdown)

#         print("Filtered markdown content saved to final_filtered_recipe.md")

#         # with open("recipe.md", "w", encoding="utf-8") as file:
#         #     file.write(markdown_content)

#         # print("Markdown content saved to recipe.md")

# if __name__ == "__main__":
#     asyncio.run(main())

import asyncio
import re
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

def read_recipe_urls(filename: str) -> list:
    """
    Reads the recipe URLs from a text file.
    For each line, if an angle bracket '<' is present, extracts the URL after it.
    Also fixes URLs that start with 'https:/' but not 'https://'.
    """
    recipe_urls = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # If the line contains an angle bracket, extract the part after it.
            if "<" in line:
                recipe_url = line.split("<")[-1]
            else:
                recipe_url = line
            # Fix URL if it starts with 'https:/' but not 'https://'
            if recipe_url.startswith("https:/") and not recipe_url.startswith("https://"):
                recipe_url = recipe_url.replace("https:/", "https://", 1)
            recipe_urls.append(recipe_url)
    return recipe_urls

def apply_filters(markdown_content: str) -> str:
    """
    Applies filtering to the markdown content:
      - Extracts only sections starting with ## or ###.
      - Skips sections containing any unwanted headings.
      - Removes markdown links.
      - Removes empty headings that start with ### or ####.
    """
    ignore_headings = [
        "#### SUBSCRIBE TO OUR RECIPES",
        "#### POPULAR RECIPES",
        "#### POPULAR CATEGORIES",
        "#### Stay in Touch",
        "#### Popular",
        "#### Search Recipes",
        "##  Rate This Recipe",
        "##  Recipe Ratings without Comment",
        "#### BROWSE BY CATEGORIES",
        "#### STAY CONNECTED",
        "#### Related Recipes",
        "#### OUR OTHER LANGUAGES",
        "#### Must Read:",
        "#### What's New"
    ]
    
    # Extract sections that start with ## or ### until the next heading or EOF
    sections = re.findall(r"(##+ .+?)(?=\n##|\n\Z)", markdown_content, re.DOTALL)
    
    cleaned_sections = []
    for section in sections:
        if any(ignored in section for ignored in ignore_headings):
            continue
        
        # Remove empty headings (lines with only ### or #### and whitespace)
        section = re.sub(r"^(#{3,4}\s*)\s*$\n", "", section, flags=re.MULTILINE)
        # Remove Markdown links
        section = re.sub(r"\[.*?\]\(.*?\)", "", section)
        cleaned_sections.append(section.strip())
    
    return "\n\n".join(cleaned_sections)

async def crawl_and_aggregate(recipe_urls: list):
    """
    Crawls each recipe URL, applies filters to the scraped markdown,
    and aggregates all filtered content into a single markdown file.
    """
    print(f"Found {len(recipe_urls)} recipe URLs to crawl.")
    
    browser_config = BrowserConfig(
        headless=True,
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
    )
    crawl_config = CrawlerRunConfig(
        markdown_generator=DefaultMarkdownGenerator()
    )
    
    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()
    
    session_id = "session1"  # reuse the same session for efficiency
    aggregated_content = []  # accumulator for all recipes
    
    try:
        for idx, url in enumerate(recipe_urls):
            print(f"Crawling {idx+1}/{len(recipe_urls)}: {url}")
            result = await crawler.arun(url=url, config=crawl_config, session_id=session_id)
            if result.success:
                print(f"Successfully crawled: {url}")
                markdown_content = result.markdown
                filtered_markdown = apply_filters(markdown_content)
                # Optionally add a header to separate recipes
                recipe_entry = f"# Recipe {idx+1}\nURL: {url}\n\n{filtered_markdown}"
                aggregated_content.append(recipe_entry)
            else:
                print(f"Failed to crawl {url}: {result.error_message}")
    finally:
        await crawler.close()
    
    # Combine all recipes with a separator and save to a single file
    final_markdown = "\n\n---\n\n".join(aggregated_content)
    with open("all_recipes.md", "w", encoding="utf-8") as f:
        f.write(final_markdown)
    print("Saved aggregated content to all_recipes.md")

async def main():
    recipe_urls = read_recipe_urls("extracted_urls.txt")
    if recipe_urls:
        await crawl_and_aggregate(recipe_urls)
    else:
        print("No recipe URLs found in the file.")

if __name__ == "__main__":
    asyncio.run(main())
