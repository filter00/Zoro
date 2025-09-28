import os
import requests

class IMDbAPI:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OMDB_API_KEY")
        self.base_url = "http://www.omdbapi.com/"

    def search(self, query: str, max_results: int = 3):
        if not self.api_key:
            return None
        try:
            params = {"apikey": self.api_key, "s": query}
            resp = requests.get(self.base_url, params=params, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            if data.get("Response") == "True":
                return data.get("Search", [])[:max_results]
            return None
        except requests.RequestException:
            return None
