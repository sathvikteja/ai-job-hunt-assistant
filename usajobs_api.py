import requests
from utils.config import USAJOBS_API_KEY, USAJOBS_EMAIL


def fetch_usajobs(keyword, location="remote", results_per_page=5):
    """
    Fetch job listings from the USAJobs API.
    """

    url = "https://data.usajobs.gov/api/search"

    headers = {
        "Host": "data.usajobs.gov",
        "User-Agent": USAJOBS_EMAIL,
        "Authorization-Key": USAJOBS_API_KEY
    }
    # handle remote search
    if location.lower() == "remote":
        location = "United States"

    params = {
        "Keyword": keyword,
        "LocationName": location,
        "ResultsPerPage": results_per_page
    }

    try:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()

            jobs = data["SearchResult"]["SearchResultItems"]

            return jobs

        else:
            print("Error:", response.status_code)
            return []

    except Exception as e:
        print("Request failed:", e)
        return []