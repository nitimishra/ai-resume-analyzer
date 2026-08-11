import os
import requests
from dotenv import load_dotenv

load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

BASE_URL = "https://api.adzuna.com/v1/api/jobs"


def fetch_jobs(query: str, location: str = "", country: str = "in", results_per_page: int = 10, page: int = 1):
    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        raise ValueError("Adzuna API credentials not found. Check your .env file.")

    url = f"{BASE_URL}/{country}/search/{page}"

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": results_per_page,
        "what": query,
        "content-type": "application/json",
    }

    if location:
        params["where"] = location

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Adzuna API request failed: {e}")
        return []

    jobs = []
    for item in data.get("results", []):
        jobs.append({
            "title": item.get("title", "N/A"),
            "company": item.get("company", {}).get("display_name", "N/A"),
            "location": item.get("location", {}).get("display_name", "N/A"),
            "description": item.get("description", ""),
            "job_url": item.get("redirect_url", "#"),
            "date_posted": item.get("created", "N/A"),
            "employment_type": item.get("contract_time", "Not specified"),
            "salary_min": item.get("salary_min"),
            "salary_max": item.get("salary_max"),
        })

    return jobs
def fetch_jooble_jobs(query: str, location: str = "India", results_per_page: int = 10, page: int = 1):
    """
    Fetch real job listings from Jooble API.
    """
    JOOBLE_API_KEY = os.getenv("JOOBLE_API_KEY")

    if not JOOBLE_API_KEY:
        raise ValueError("Jooble API key not found. Check your .env file.")

    url = f"https://jooble.org/api/{JOOBLE_API_KEY}"

    payload = {
        "keywords": query,
        "location": location,
        "page": str(page)
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Jooble API request failed: {e}")
        return []

    jobs = []
    for item in data.get("jobs", [])[:results_per_page]:
        jobs.append({
            "title": item.get("title", "N/A"),
            "company": item.get("company", "N/A"),
            "location": item.get("location", "N/A"),
            "description": item.get("description", "").replace("<b>", "").replace("</b>", ""),
            "job_url": item.get("link", "#"),
            "date_posted": item.get("updated", "N/A"),
            "employment_type": item.get("type", "Not specified"),
            "salary_min": None,
            "salary_max": None,
        })

    return jobs
def fetch_all_jobs(query: str, location: str = "india", results_per_page: int = 10, page: int = 1):
    """
    Fetches jobs from both Adzuna and Jooble, combines and deduplicates them.
    """
    adzuna_jobs = fetch_jobs(query=query, location=location, results_per_page=results_per_page, page=page)
    jooble_jobs = fetch_jooble_jobs(query=query, location=location, results_per_page=results_per_page, page=page)

    all_jobs = adzuna_jobs + jooble_jobs

    # Simple deduplication based on title + company
    seen = set()
    unique_jobs = []
    for job in all_jobs:
        key = (job['title'].strip().lower(), job['company'].strip().lower())
        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)

    return unique_jobs