# import asyncio
# import re
# import requests
# from typing import List, Set
# from xml.etree import ElementTree

# def get_sitemap_urls() -> List[str]:
#     """
#     Fetches cuisine URLs from the Hebbar's Kitchen cuisines sitemap.
#     Example output URL: https://hebbarskitchen.com/cuisines/gujarat/
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

# def expand_pagination(cuisine_url: str) -> List[str]:
#     """
#     Given a cuisine URL (e.g. https://hebbarskitchen.com/cuisines/gujarat/),
#     returns a list of paginated URLs (page/1 is the main page).
#     Stops when a page returns a non-200 status code.
#     """
#     pages = []
#     page = 1
#     while True:
#         if page == 1:
#             url = cuisine_url.rstrip('/')
#         else:
#             url = cuisine_url.rstrip('/') + f"/page/{page}/"
#         try:
#             response = requests.get(url)
#             if response.status_code == 200:
#                 pages.append(url)
#                 page += 1
#             else:
#                 break
#         except Exception as e:
#             print(f"Error accessing {url}: {e}")
#             break
#     return pages

# def extract_recipe_urls_from_html(html: str) -> List[str]:
#     """
#     Extracts recipe URLs from HTML content.
#     We assume that recipe URLs start with "https://hebbarskitchen.com/"
#     and exclude any URLs that contain "/cuisines/".
#     """
#     # This regex finds href values that begin with https://hebbarskitchen.com/
#     links = re.findall(r'href="(https://hebbarskitchen\.com/[^"]+)"', html)
#     recipe_links = []
#     for link in links:
#         if "/cuisines/" not in link:
#             recipe_links.append(link)
#     return list(set(recipe_links))

# async def fetch_page(url: str) -> (int, str):
#     """
#     Asynchronously fetches a URL using requests in a thread.
#     Returns a tuple: (status_code, text).
#     """
#     loop = asyncio.get_event_loop()
#     def get_url():
#         resp = requests.get(url)
#         return resp.status_code, resp.text
#     return await loop.run_in_executor(None, get_url)

# async def main():
#     # Get all cuisine URLs from the sitemap.
#     cuisine_urls = get_sitemap_urls()
#     if not cuisine_urls:
#         print("No cuisine URLs found.")
#         return

#     all_recipe_urls: Set[str] = set()
#     print(f"Found {len(cuisine_urls)} cuisine URLs in the sitemap.")

#     # For each cuisine URL, expand its pagination and extract recipe URLs.
#     for cuisine_url in cuisine_urls:
#         print(f"\nProcessing cuisine: {cuisine_url}")
#         paginated_urls = expand_pagination(cuisine_url)
#         print(f"  Found {len(paginated_urls)} paginated pages.")
#         for page_url in paginated_urls:
#             print(f"    Fetching page: {page_url}")
#             status, html = await fetch_page(page_url)
#             if status == 200:
#                 recipe_links = extract_recipe_urls_from_html(html)
#                 print(f"      Extracted {len(recipe_links)} recipe URLs.")
#                 all_recipe_urls.update(recipe_links)
#             else:
#                 print(f"      Failed to fetch page: {page_url} (status: {status})")

#     # Save all unique recipe URLs to a markdown file.
#     output_file = "all_recipe_urls.md"
#     with open(output_file, "w", encoding="utf-8") as f:
#         f.write("# Recipe URLs\n\n")
#         for url in sorted(all_recipe_urls):
#             f.write(f"- {url}\n")
#     print(f"\nSaved {len(all_recipe_urls)} unique recipe URLs to '{output_file}'.")

# if __name__ == "__main__":
#     asyncio.run(main())


import asyncio
import re
import requests
from typing import List, Set
from xml.etree import ElementTree

# Hardcoded list of cuisine URLs
CUISINE_URLS = [
    "https://hebbarskitchen.com/cuisines/andhra/",
    "https://hebbarskitchen.com/cuisines/awadh/",
    "https://hebbarskitchen.com/cuisines/bangalore/",
    "https://hebbarskitchen.com/cuisines/bengali/",
    "https://hebbarskitchen.com/cuisines/goan/",
    "https://hebbarskitchen.com/cuisines/gujarat/",
    "https://hebbarskitchen.com/cuisines/hyderabad/",
    "https://hebbarskitchen.com/cuisines/karnataka/",
    "https://hebbarskitchen.com/cuisines/kashmir/",
    "https://hebbarskitchen.com/cuisines/kerala/",
    "https://hebbarskitchen.com/cuisines/konkan/",
    "https://hebbarskitchen.com/cuisines/maharashtra/",
    "https://hebbarskitchen.com/cuisines/mangalore/",
    "https://hebbarskitchen.com/cuisines/mysore/",
    "https://hebbarskitchen.com/cuisines/north-indian/",
    "https://hebbarskitchen.com/cuisines/north-karnataka/",
    "https://hebbarskitchen.com/cuisines/punjabi/",
    "https://hebbarskitchen.com/cuisines/rajasthani/",
    "https://hebbarskitchen.com/cuisines/south-indian/",
    "https://hebbarskitchen.com/cuisines/tamil-cuisine/",
    "https://hebbarskitchen.com/cuisines/udupi/"
]

def expand_pagination(cuisine_url: str) -> List[str]:
    """
    Given a cuisine URL (e.g. https://hebbarskitchen.com/cuisines/gujarat/),
    returns a list of paginated URLs (page/1 is the main page).
    Stops when a page returns a non-200 status code.
    """
    pages = []
    page = 1
    while True:
        if page == 1:
            url = cuisine_url.rstrip('/')
        else:
            url = cuisine_url.rstrip('/') + f"/page/{page}/"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                pages.append(url)
                page += 1
            else:
                break
        except Exception as e:
            print(f"Error accessing {url}: {e}")
            break
    return pages

def extract_recipe_urls_from_html(html: str) -> List[str]:
    """
    Extracts recipe URLs from HTML content.
    Assumes that recipe URLs start with "https://hebbarskitchen.com/"
    and excludes any URLs that contain "/cuisines/".
    Also ignores URLs that end with "-hi/" or "-kn/".
    """
    links = re.findall(r'href="(https://hebbarskitchen\.com/[^"]+)"', html)
    recipe_links = []
    for link in links:
        if "/cuisines/" in link:
            continue
        if link.endswith("-hi/") or link.endswith("-kn/"):
            continue
        recipe_links.append(link)
    return list(set(recipe_links))

async def fetch_page(url: str) -> (int, str):
    """
    Asynchronously fetches a URL using requests in a thread.
    Returns a tuple: (status_code, text).
    """
    loop = asyncio.get_event_loop()
    def get_url():
        resp = requests.get(url)
        return resp.status_code, resp.text
    return await loop.run_in_executor(None, get_url)

async def main():
    all_recipe_urls: Set[str] = set()
    print(f"Processing {len(CUISINE_URLS)} cuisine URLs.")

    # Process each cuisine URL
    for cuisine_url in CUISINE_URLS:
        print(f"\nProcessing cuisine: {cuisine_url}")
        paginated_urls = expand_pagination(cuisine_url)
        print(f"  Found {len(paginated_urls)} paginated pages for {cuisine_url}.")
        for page_url in paginated_urls:
            print(f"    Fetching page: {page_url}")
            status, html = await fetch_page(page_url)
            if status == 200:
                recipe_links = extract_recipe_urls_from_html(html)
                print(f"      Extracted {len(recipe_links)} recipe URLs.")
                all_recipe_urls.update(recipe_links)
            else:
                print(f"      Failed to fetch page: {page_url} (status: {status})")
    
    # Save all unique recipe URLs to a markdown file.
    output_file = "all_recipe_urls.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Recipe URLs\n\n")
        for url in sorted(all_recipe_urls):
            f.write(f"- {url}\n")
    print(f"\nSaved {len(all_recipe_urls)} unique recipe URLs to '{output_file}'.")

if __name__ == "__main__":
    asyncio.run(main())
