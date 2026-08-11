import requests

BASE_URL = "https://ai-resume-analyzer-backend-zo1q.onrender.com"


def api_signup(name, email, password):
    try:
        response = requests.post(
            f"{BASE_URL}/signup",
            json={"name": name, "email": email, "password": password}
        )
        if response.status_code == 200:
            return True, response.json().get("message", "Account created successfully!")
        else:
            return False, response.json().get("detail", "Signup failed.")
    except requests.exceptions.RequestException as e:
        return False, f"Could not connect to server: {e}"


def api_login(email, password):
    try:
        response = requests.post(
            f"{BASE_URL}/login",
            json={"email": email, "password": password}
        )
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException:
        return None


def api_upload_resume(uploaded_file):
    try:
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        response = requests.post(f"{BASE_URL}/upload-resume", files=files)
        if response.status_code == 200:
            return response.json().get("resume_text", ""), None
        else:
            return None, response.json().get("detail", "Upload failed.")
    except requests.exceptions.RequestException as e:
        return None, f"Could not connect to server: {e}"


def api_analyze_resume(resume_text):
    try:
        response = requests.post(
            f"{BASE_URL}/analyze-resume",
            json={"resume_text": resume_text}
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {}
    except requests.exceptions.RequestException:
        return {}


def api_search_jobs(query, location="india", page=1):
    try:
        response = requests.post(
            f"{BASE_URL}/jobs",
            json={"query": query, "location": location, "page": page}
        )
        if response.status_code == 200:
            return response.json().get("jobs", [])
        else:
            return []
    except requests.exceptions.RequestException:
        return []


def api_match_job(resume_analysis, job_description):
    try:
        response = requests.post(
            f"{BASE_URL}/match-job",
            json={"resume_analysis": resume_analysis, "job_description": job_description}
        )
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException:
        return None