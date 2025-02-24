# import asyncio
# import re
# from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
# from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

# def extract_recipe_links(markdown_file: str) -> list:
#     """
#     Extracts valid recipe URLs from the given markdown file.
#     """
#     with open(markdown_file, "r", encoding="utf-8") as f:
#         markdown_content = f.read()
    
#     # Regex to find URLs in markdown
#     urls = re.findall(r"https://hebbarskitchen\.com/[\w\-/]+", markdown_content)
    
#     # Remove duplicates and invalid URLs
#     return list(set(urls))

# def apply_filters(markdown_content: str) -> str:
#     """
#     Filters unwanted content from markdown:
#       - Removes specific unwanted headings
#       - Removes markdown links
#       - Removes empty headings
#     """
#     ignore_headings = [
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
#     ]
    
#     # Extract sections that start with ## or ### until the next heading or EOF
#     sections = re.findall(r"(##+ .+?)(?=\n##|\n\Z)", markdown_content, re.DOTALL)
    
#     cleaned_sections = []
#     for section in sections:
#         if any(ignored in section for ignored in ignore_headings):
#             continue
        
#         # Remove empty headings (e.g., `###` with no text)
#         section = re.sub(r"^(#{3,4}\s*)\s*$\n", "", section, flags=re.MULTILINE)
        
#         # Remove markdown links like [text](url)
#         section = re.sub(r"\[.*?\]\(.*?\)", "", section)
        
#         cleaned_sections.append(section.strip())
    
#     return "\n\n".join(cleaned_sections)

# async def crawl_recipes(recipe_urls: list):
#     """
#     Crawls recipe pages, applies filtering, and saves each to a markdown file.
#     """
#     browser_config = BrowserConfig(
#         headless=True,
#         extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
#     )
#     crawl_config = CrawlerRunConfig(
#         markdown_generator=DefaultMarkdownGenerator()
#     )
    
#     crawler = AsyncWebCrawler(config=browser_config)
#     await crawler.start()

#     session_id = "session1"  # Keep a single session for efficiency

#     try:
#         for idx, url in enumerate(recipe_urls):
#             print(f"Crawling {idx+1}/{len(recipe_urls)}: {url}")
#             result = await crawler.arun(url=url, config=crawl_config, session_id=session_id)
#             if result.success:
#                 print(f"Successfully crawled: {url}")
                
#                 # Get the raw markdown
#                 markdown_content = result.markdown
                
#                 # Apply filtering
#                 filtered_markdown = apply_filters(markdown_content)
                
#                 # Generate a filename
#                 filename = f"recipe_{idx+1}.md"
                
#                 # Save to file
#                 with open(filename, "w", encoding="utf-8") as f:
#                     f.write(filtered_markdown)
                
#                 print(f"Saved: {filename}")
#             else:
#                 print(f"Failed to crawl {url}: {result.error_message}")
#     finally:
#         await crawler.close()

# async def main():
#     markdown_file = "recipes.md"  # Your input markdown file
#     recipe_links = extract_recipe_links(markdown_file)
#     print(f"Found {len(recipe_links)} recipes.")
    
#     if recipe_links:
#         await crawl_recipes(recipe_links)
#     else:
#         print("No valid recipe links found.")

# if __name__ == "__main__":
#     asyncio.run(main())



import asyncio
import re
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

def extract_recipe_links(markdown_file: str) -> list:
    """
    Extracts valid recipe URLs from the given markdown file.
    """
    with open(markdown_file, "r", encoding="utf-8") as f:
        markdown_content = f.read()
    
    # Regex to find URLs in markdown
    urls = re.findall(r"https://hebbarskitchen\.com/[\w\-/]+", markdown_content)
    
    # Remove duplicates and invalid URLs
    return list(set(urls))

def apply_filters(markdown_content: str) -> str:
    """
    Filters unwanted content from markdown:
      - Removes specific unwanted headings
      - Removes markdown links
      - Removes empty headings
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
        
        # Remove empty headings (e.g., `###` with no text)
        section = re.sub(r"^(#{3,4}\s*)\s*$\n", "", section, flags=re.MULTILINE)
        
        # Remove markdown links like [text](url)
        section = re.sub(r"\[.*?\]\(.*?\)", "", section)
        
        cleaned_sections.append(section.strip())
    
    return "\n\n".join(cleaned_sections)

async def crawl_recipes(recipe_urls: list):
    """
    Crawls recipe pages, applies filtering, and appends all the content to a single markdown file.
    """
    browser_config = BrowserConfig(
        headless=True,
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
    )
    crawl_config = CrawlerRunConfig(
        markdown_generator=DefaultMarkdownGenerator()
    )
    
    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()

    session_id = "session1"  # Keep a single session for efficiency
    all_recipes_content = []  # Accumulator for all recipes
    
    try:
        for idx, url in enumerate(recipe_urls):
            print(f"Crawling {idx+1}/{len(recipe_urls)}: {url}")
            result = await crawler.arun(url=url, config=crawl_config, session_id=session_id)
            if result.success:
                print(f"Successfully crawled: {url}")
                
                # Get the raw markdown
                markdown_content = result.markdown
                
                # Apply filtering
                filtered_markdown = apply_filters(markdown_content)
                
                # Optionally add a header for each recipe
                header = f"# Recipe {idx+1}\nURL: {url}\n"
                full_recipe = f"{header}\n{filtered_markdown}"
                
                all_recipes_content.append(full_recipe)
            else:
                print(f"Failed to crawl {url}: {result.error_message}")
    finally:
        await crawler.close()
    
    # Combine all recipes with a separator and save to a single markdown file
    final_content = "\n\n---\n\n".join(all_recipes_content)
    with open("all_recipes.md", "w", encoding="utf-8") as f:
        f.write(final_content)
    print("Saved all filtered recipes to all_recipes.md")

async def main():
    markdown_file = "cleaned_recipe_urls.md"  # Your input markdown file with URLs
    recipe_links = extract_recipe_links(markdown_file)
    print(f"Found {len(recipe_links)} recipes.")
    
    if recipe_links:
        await crawl_recipes(recipe_links)
    else:
        print("No valid recipe links found.")

if __name__ == "__main__":
    asyncio.run(main())
