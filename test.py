from job_api import fetch_jobs

jobs = fetch_jobs(query="python developer", location="delhi")
print(f"Found {len(jobs)} jobs")
for job in jobs[:2]:
    print(job["title"], "-", job["company"])
    print(job["job_url"])
    print("---")