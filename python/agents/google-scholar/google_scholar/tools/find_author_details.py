"""Tool to search google scholar for detailed information on an author."""

import os
import requests

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

def find_author_details_tool(author_id: str) -> dict:
    """ Retrieves detailed information for a specific Google Scholar author profile.

    Args:
        author_id: The unique ID of the author (e.g., "2EpSYrcAAAAJ").

    Returns:
        A dictionary containing the author's details 
        (name, google scholar profile url, affiliations, interests)
        and a list of their articles. Returns an empty dictionary if not found or an error occurs.
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

        if "author" in results:
            author_data = results["author"]
            author_details = {
                "name": author_data.get("name", "N/A"),
                "author profile": author_data.get("google_scholar_author_url", "N/A"),
                "affiliations": author_data.get("affiliations", "N/A"),
                "interests": [
                    interest.get("title", "N/A")
                    for interest in author_data.get("interests", [])
                ]
            }

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

        return {"author": author_details, "articles": processed_articles}

    except requests.exceptions.RequestException as e:
        print(f"A request error occurred: {e}")
        return {"error": f"Request error: {e}"}
    except Exception as e:
        print(f"An unexpected non-requests error occurred: {e}")
        return {"error": f"Unexpected error: {e}"}
