import requests
import os 

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

def search_google_scholar(query: str) -> dict:
    """
    Performs a search on Google Scholar using SerpApi, limiting results to 5 articles
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

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": f"Unexpected error: {e}"}
    
def search_google_news(query: str) -> dict:
    """
    Performs a search on Google News using SerpApi, limiting results to 5 articles
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
                    # Google News results might not have 'publication_info' or 'citation' in the same way as Scholar
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
    """
    performs a search on Google scholar to search for profiles

    retuns:
    name, link to profile, author_id, and affiliations of the top 5 results
    """
    base_url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_scholar_profiles",
        "mauthors": name,
        "api_key": SERPAPI_API_KEY, 
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() 
        results = response.json()

        processed_authors = []
        if "profiles" in results:
            num =0
            for result in results["profiles"]:
                author_info = {
                    "name": result.get("name", "N/A"),
                    "link": result.get("link", "N/A"),
                    "author id": result.get("author_id", "N/A"),
                    "affiliations": result.get("affiliations", {})
                }
                processed_authors.append(author_info)
                num+=1
                if num >=5:
                    break
        
        return {"Authors": processed_authors}

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": f"Unexpected error: {e}"}
    
