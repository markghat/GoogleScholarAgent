import requests
import os

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

def search_google_scholar(query: str) -> dict:
    """Performs a search on Google Scholar using SerpApi, limiting results to 5 articles
    and returning only specific details (link, title, snippet, citation).

    Args:
        query: The search query string.

    Returns:
        A dictionary containing a list of up to 5 simplified article results.
        Each article dictionary will have 'link', 'title', 'snippet', and 'citation'.
        Returns an empty dictionary if the request fails or no results are found.
    """
    base_url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_scholar",
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "num": 5, 
    }

    try:
        response = requests.get(base_url, params=params)
        search_results = response.json()

        processed_articles = []
        if "organic_results" in search_results:
            for result in search_results["organic_results"]:
                article_info = {
                    "title": result.get("title", "N/A"),
                    "link": result.get("link", "N/A"),
                    "snippet": result.get("snippet", "N/A"),
                    "citation": result.get("publication_info", {}).get("summary", "N/A")
                }
                processed_articles.append(article_info)

        return {"articles": processed_articles}

    except requests.exceptions.RequestException as e:
        print(f"A request error occurred: {e}")
        return {"error": f"Request error: {e}"}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": f"Unexpected error: {e}"}

def find_author(name: str) -> dict:
    """performs a search on Google scholar to search for Authors

    args:
    author name

    returns:
    name, link to profile, author_id,
    """

    base_url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_scholar",
        "q": f"author:{name}",
        "api_key": SERPAPI_API_KEY,
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() 
        results = response.json()

        found_authors = []
        if "profiles" in results and "authors" in results["profiles"]:
            for author_data in results["profiles"]["authors"]:
                author_profile = {
                    "name": author_data.get("name", "N/A"),
                    "link": author_data.get("link", "N/A"),
                    "author_id": author_data.get("author_id", "N/A"),
                    # "email": author_data.get("email", "N/A"),
                    # "cited_by": author_data.get("cited_by", "N/A")
                }
                found_authors.append(author_profile)
        else:
            print("DEBUG: 'profiles' or 'authors' key NOT found in SerpApi response for author search.")
        return {"Authors": found_authors}

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": f"Unexpected error: {e}"}

def find_author_details(author_id: str) -> dict:
    """ Retrieves detailed information for a specific Google Scholar author profile.

    Args:
        author_id: The unique ID of the author (e.g., "2EpSYrcAAAAJ").

    Returns:
        A dictionary containing the author's details (name, affiliations, interests)
        and a list of their articles. Returns an empty dictionary if not found or an error occurs.
    """

    base_url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_scholar_author",  
        "author_id": author_id,             
        "api_key": SERPAPI_API_KEY,
    }
    try:

        response = requests.get(base_url, params=params)
        response.raise_for_status() 
        results = response.json()


        author_details = {}
        processed_articles = []

        if "author" in results:
            author_data = results["author"]
            author_details = {
                "name": author_data.get("name", "N/A"),
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

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": f"Unexpected error: {e}"}





    
def search_google_news(query: str) -> dict:

    """Performs a search on Google News using SerpApi, limiting results to 5 articles
    and returning only specific details (link, title, snippet).

    Args:
        query: The search query string.

    Returns:
        A dictionary containing a list of up to 5 simplified news article results.
        Each article dictionary will have 'link', 'title', and 'author'.
        Returns an empty dictionary if the request fails or no results are found.
    """
    base_url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_news", 
        "q":query, 
        "api_key": SERPAPI_API_KEY,
        "num": 5,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        search_results = response.json()

        processed_articles = []
        if "news_results" in search_results:
            for result in search_results["news_results"]:
                article_info = {
                    "title": result.get("title", "N/A"),
                    "link": result.get("link", "N/A"),
                    "author": result.get("author", "N/A")
                }
                processed_articles.append(article_info)
        
        return {"articles": processed_articles}

    except requests.exceptions.RequestException as e:
        print(f"A request error occurred: {e}")
        return {"error": f"Request error: {e}"}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": f"Unexpected error: {e}"}

