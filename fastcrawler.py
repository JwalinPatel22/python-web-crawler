# import asyncio
# import re
# import requests
# from typing import List
# from xml.etree import ElementTree
# from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
# from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

# def get_sitemap_urls() -> List[str]:
#     """
#     Fetches URLs from the sitemap (in this case, Hebbar's Kitchen recipe sitemap).
#     """
#     sitemap_url = "https://hebbarskitchen.com/cuisines-sitemap.xml"
#     try:
#         response = requests.get(sitemap_url)
#         response.raise_for_status()
#         root = ElementTree.fromstring(response.content)
#         namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
#         urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]
#         return urls
#     except Exception as e:
#         print(f"Error fetching sitemap: {e}")
#         return []

# def apply_filters(markdown_content: str) -> str:
#     """
#     Applies filtering to the markdown content:
#       - Extracts only sections starting with ## or ###.
#       - Skips sections containing any unwanted headings.
#       - Removes markdown links.
#       - Removes empty headings that start with ### or ####.
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
    
#     # Extract sections that start with ## or ### until the next section or end of text
#     sections = re.findall(r"(##+ .+?)(?=\n##|\n\Z)", markdown_content, re.DOTALL)
    
#     cleaned_sections = []
#     for section in sections:
#         # Skip the section if it contains any of the ignored headings
#         if any(ignored in section for ignored in ignore_headings):
#             continue
        
#         # Remove empty headings that start with ### or ####.
#         # This regex removes lines that start with 3 or 4 '#' and have no text (only whitespace) after them.
#         section = re.sub(r"^(#{3,4}\s*)\s*$\n", "", section, flags=re.MULTILINE)
        
#         # Remove Markdown links of the form [text](url)
#         section = re.sub(r"\[.*?\]\(.*?\)", "", section)
        
#         cleaned_sections.append(section.strip())
    
#     final_markdown = "\n\n".join(cleaned_sections)
#     return final_markdown

# async def crawl_and_filter(urls: List[str]):
#     """
#     Crawls each URL from the sitemap, applies the markdown filters,
#     and saves each filtered result into a separate markdown file.
#     """
#     print(f"Found {len(urls)} URLs to crawl")
    
#     # Configure browser and crawler settings
#     browser_config = BrowserConfig(
#         headless=True,
#         extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
#     )
    
#     crawl_config = CrawlerRunConfig(
#         markdown_generator=DefaultMarkdownGenerator()
#     )
    
#     # Create and start the crawler
#     crawler = AsyncWebCrawler(config=browser_config)
#     await crawler.start()
    
#     session_id = "session1"  # reuse the same session across all URLs
#     try:
#         for idx, url in enumerate(urls):
#             print(f"Crawling URL {idx+1}/{len(urls)}: {url}")
#             result = await crawler.arun(
#                 url=url,
#                 config=crawl_config,
#                 session_id=session_id
#             )
#             if result.success:
#                 print(f"Successfully crawled: {url}")
#                 # Get the raw markdown content
#                 markdown_content = result.markdown
#                 # Apply our filters to the markdown
#                 filtered_markdown = apply_filters(markdown_content)
#                 # Save the filtered markdown to a file (naming each file uniquely)
#                 filename = f"final_filtered_recipe_{idx+1}.md"
#                 with open(filename, "w", encoding="utf-8") as f:
#                     f.write(filtered_markdown)
#                 print(f"Saved filtered content to {filename}")
#             else:
#                 print(f"Failed: {url} - Error: {result.error_message}")
#     finally:
#         await crawler.close()

# async def main():
#     urls = get_sitemap_urls()
#     if urls:
#         await crawl_and_filter(urls)
#     else:
#         print("No URLs found to crawl")

# if __name__ == "__main__":
#     asyncio.run(main())





# import requests
# from xml.etree import ElementTree

# def get_sitemap_urls():
#     """
#     Fetches URLs from the sitemap (Hebbar's Kitchen recipe sitemap) and saves them to a text file.
#     """
#     sitemap_url = "https://hebbarskitchen.com/cuisines-sitemap.xml"
#     try:
#         response = requests.get(sitemap_url)
#         response.raise_for_status()
#         root = ElementTree.fromstring(response.content)
#         namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
#         urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]

#         # Append URLs to a text file
#         with open("recipe_urls.txt", "a", encoding="utf-8") as file:
#             for url in urls:
#                 file.write(url + "\n")

#         print(f"Successfully saved {len(urls)} URLs to recipe_urls.txt")

#     except Exception as e:
#         print(f"Error fetching sitemap: {e}")

# if __name__ == "__main__":
#     get_sitemap_urls()





import asyncio
import re
import requests
from typing import List
from xml.etree import ElementTree
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

def get_sitemap_urls() -> List[str]:
    """
    Fetches URLs from the sitemap (in this case, Hebbar's Kitchen cuisine sitemap).
    """
    sitemap_url = "https://hebbarskitchen.com/cuisines-sitemap.xml"
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        root = ElementTree.fromstring(response.content)
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]
        return urls
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return []

def extract_cuisine_name(url: str) -> str:
    """
    Extracts the cuisine name from the URL.
    Example: 'https://hebbarskitchen.com/cuisines/gujarat/' -> 'gujarat'
    """
    return url.rstrip('/').split("/")[-1]

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
    
    sections = re.findall(r"(##+ .+?)(?=\n##|\n\Z)", markdown_content, re.DOTALL)
    
    cleaned_sections = []
    for section in sections:
        if any(ignored in section for ignored in ignore_headings):
            continue
        
        section = re.sub(r"^(#{3,4}\s*)\s*$\n", "", section, flags=re.MULTILINE)
        section = re.sub(r"\[.*?\]\(.*?\)", "", section)
        
        cleaned_sections.append(section.strip())
    
    final_markdown = "\n\n".join(cleaned_sections)
    return final_markdown

async def crawl_and_filter(urls: List[str]):
    """
    Crawls each URL from the sitemap, applies the markdown filters,
    and appends all filtered content into a single markdown file.
    """
    print(f"Found {len(urls)} URLs to crawl")
    
    browser_config = BrowserConfig(
        headless=True,
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
    )
    
    crawl_config = CrawlerRunConfig(
        markdown_generator=DefaultMarkdownGenerator()
    )
    
    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()
    
    session_id = "session1"  # reuse the same session across all URLs
    all_content = []  # list to accumulate content from each crawl
    
    try:
        for idx, url in enumerate(urls):
            cuisine_name = extract_cuisine_name(url)
            print(f"Crawling {idx+1}/{len(urls)}: {url} (Cuisine: {cuisine_name})")
            
            result = await crawler.arun(
                url=url,
                config=crawl_config,
                session_id=session_id
            )
            if result.success:
                print(f"Successfully crawled: {url}")
                markdown_content = result.markdown
                filtered_markdown = apply_filters(markdown_content)
                # Optionally, prepend a heading with the cuisine name for separation
                content_with_heading = f"# {cuisine_name.capitalize()}\n\n{filtered_markdown}"
                all_content.append(content_with_heading)
            else:
                print(f"Failed: {url} - Error: {result.error_message}")
    finally:
        await crawler.close()
    
    # Append all content to a single markdown file
    final_content = "\n\n---\n\n".join(all_content)
    with open("all_cuisines.md", "w", encoding="utf-8") as f:
        f.write(final_content)
    print("Saved all filtered content to all_cuisines.md")

async def main():
    urls = get_sitemap_urls()
    if urls:
        await crawl_and_filter(urls)
    else:
        print("No URLs found to crawl")

if __name__ == "__main__":
    asyncio.run(main())
