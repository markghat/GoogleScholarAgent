"""Tool to search google scholar for detailed information on an author."""

import os
import requests
from bs4 import BeautifulSoup
import re

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

def _scrape_article_links_from_profile(profile_url: str) -> list[str]:
    """
    Scrapes an author's Google Scholar profile page to find direct article links.

    Args:
        profile_url (str): The URL of the Google Scholar author profile page.

    Returns:
        list[str]: A list of unique article URLs found on the profile page.
    """
    article_links = set()
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(profile_url, headers=headers, timeout=1)
        response.raise_for_status() 

        soup = BeautifulSoup(response.text, 'html.parser')

        for link_tag in soup.find_all('a', class_='gsc_a_at'):
            href = link_tag.get('href')
            if href:
                if not href.startswith('http'):
                    full_url = f"https://scholar.google.com{href}"
                else:
                    full_url = href
                
                if "view_article" in full_url: 
                    article_links.add(full_url)

    except requests.exceptions.RequestException as e:
        print(f"Error scraping profile URL {profile_url}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during profile scraping: {e}")

    return sorted(list(article_links))


def find_author_details_tool(author_id: str) -> dict:
    """ Retrieves detailed information for a specific Google Scholar author profile
        and scrapes article links directly from the author's profile page.

    Args:
        author_id: The unique ID of the author (e.g., "2EpSYrcAAAAJ").

    Returns:
        A dictionary containing the author's details 
        (name, thumbnail, author profile url, affiliations, interests),
        a list of their articles (from SerpApi), and a list of scraped article links.
        Returns an empty dictionary if not found or an error occurs.
    """

    base_url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_scholar_author",  
        "author_id": author_id,
        "api_key": SERPAPI_API_KEY,
        "as_sdt": "as_vis"
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        results = response.json()

        author_details = {}
        processed_articles = []
        scraped_article_urls = []

        if "author" in results:
            author_data = results["author"]
            author_details = {
                "name": author_data.get("name", "N/A"),
                "author image": author_data.get("thumbnail", "N/A")
                if author_data.get("thumbnail") != "https://scholar.google.com/citations/images/avatar_scholar_128.png"
                else "N/A", 
                "affiliations": author_data.get("affiliations", "N/A"),
                "interests": [
                    interest.get("title", "N/A")
                    for interest in author_data.get("interests", [])
                ]
            }
            
        author_profile_url = results["search_metadata"].get("google_scholar_author_url", "N/A")
        author_details["author profile url"] = author_profile_url
        print(f"DEBUG: Author profile URL: {author_profile_url}")
     
        if author_profile_url and author_profile_url != "N/A":
            scraped_article_urls = _scrape_article_links_from_profile(author_profile_url)
   

        if "articles" in results:
            for article in results["articles"][:5]:
                processed_articles.append({
                    "title": article.get("title", "N/A"),
                    "link": article.get("link", "N/A"),
                    "authors": article.get("authors", "N/A"),
                    "publication": article.get("publication", "N/A"),
                    "cited_by_value": article.get("cited_by", {}).get("value", "N/A"),
                    "year": article.get("year", "N/A")
                })

        return {
            "author": author_details,
            "articles": processed_articles,
            "scraped_article_links": scraped_article_urls
        }

    except requests.exceptions.RequestException as e:
        print(f"A request error occurred: {e}")
        return {"error": f"Request error: {e}"}
    except Exception as e:
        print(f"An unexpected non-requests error occurred: {e}")
        return {"error": f"Unexpected error: {e}"}


if __name__ == "__main__":
    if not SERPAPI_API_KEY:
        print("SERPAPI_API_KEY environment variable not set. Please set it to run the example.")
    else:
        test_author_id = "2EpSYrcAAAAJ"
        print(f"Searching for author details and scraping article links for ID: {test_author_id}")
        details = find_author_details_tool(test_author_id)

        if "error" in details:
            print(f"An error occurred: {details['error']}")
        else:
            print("\n--- Author Details ---")
            for key, value in details["author"].items():
                print(f"{key}: {value}")

            print("\n--- Articles (from SerpApi) ---")
            if details["articles"]:
                for i, article in enumerate(details["articles"]):
                    print(f"Article {i+1}:")
                    for k, v in article.items():
                        print(f"  {k}: {v}")
            else:
                print("No articles found via SerpApi.")
            
            print("\n--- Scraped Article Links (from profile page) ---")
            if details["scraped_article_links"]:
                for i, link in enumerate(details["scraped_article_links"]):
                    print(f"Link {i+1}: {link}")
            else:
                print("No additional article links scraped from the profile page.")
