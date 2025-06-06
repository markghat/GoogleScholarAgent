import requests
import json
import os # Import the os module to access environment variables

# Assuming these imports are available from your Google Agent Development Kit framework
# If not, you might need to adjust how the tool is registered or defined.
# from google_generative_ai.tools import Tool, register_tool

# For demonstration purposes, we'll define a placeholder for register_tool
# In a real framework, this would likely be provided by the SDK.
def register_tool(func):
    """
    A placeholder decorator for registering tools.
    In a real Google Agent Development Kit, this would handle tool registration.
    """
    print(f"Tool '{func.__name__}' registered successfully.")
    return func

# Your SerpApi API Key - now loaded from environment variables
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

@register_tool
def google_scholar_search(query: str) -> dict:
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
    if not SERPAPI_API_KEY:
        error_msg = "SERPAPI_API_KEY environment variable not set. Cannot perform search."
        print(f"Error: {error_msg}")
        return {"error": error_msg}

    base_url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_scholar",
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "num": 5, # Limit the number of results to 5
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        search_results = response.json()

        # Process and filter the organic results
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
                if len(processed_articles) >= 5: # Ensure we don't exceed 5 articles
                    break
        
        return {"articles": processed_articles}

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.text}")
        return {"error": f"HTTP error: {http_err}", "details": response.text}
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
        return {"error": f"Connection error: {conn_err}"}
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
        return {"error": f"Timeout error: {timeout_err}"}
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred during the request: {req_err}")
        return {"error": f"Request error: {req_err}"}
    except json.JSONDecodeError as json_err:
        print(f"Failed to decode JSON response: {json_err}")
        print(f"Raw response: {response.text}")
        return {"error": f"JSON decode error: {json_err}", "raw_response": response.text}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": f"Unexpected error: {e}"}
