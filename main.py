from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from resume_parser import extract_resume_text
from resume_analyzer import analyze_resume
from job_api import fetch_all_jobs
from job_analyzer import analyze_job
from job_matcher import calculate_match
from recommendations import generate_recommendations
from fastapi.middleware.cors import CORSMiddleware

from database import create_database, register_user, login_user

app = FastAPI(title="ResumeAI Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database table on startup
create_database()


# ============================================================
# REQUEST MODELS (data validation)
# ============================================================

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str

class ResumeTextRequest(BaseModel):
    resume_text: str


class JobSearchRequest(BaseModel):
    query: str
    location: str = "india"
    page: int = 1


class MatchRequest(BaseModel):
    resume_analysis: dict
    job_description: str


# ============================================================
# ROOT (health check)
# ============================================================

@app.get("/")
def root():
    return {"status": "ResumeAI backend is running"}


# ============================================================
# AUTH ENDPOINTS
# ============================================================

@app.post("/signup")
def signup(data: SignupRequest):
    success, message = register_user(data.name, data.email, data.password)

    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {"message": message}


@app.post("/login")
def login(data: LoginRequest):
    user = login_user(data.email, data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    return user

# ============================================================
# RESUME ENDPOINTS
# ============================================================

@app.post("/analyze-resume")
def analyze_resume_endpoint(data: ResumeTextRequest):
    if not data.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text is empty.")

    try:
        result = analyze_resume(data.resume_text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume analysis failed: {e}")


# ============================================================
# JOB ENDPOINTS
# ============================================================

@app.post("/jobs")
def search_jobs_endpoint(data: JobSearchRequest):
    try:
        jobs = fetch_all_jobs(query=data.query, location=data.location, page=data.page)
        return {"jobs": jobs, "count": len(jobs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job search failed: {e}")


@app.post("/match-job")
def match_job_endpoint(data: MatchRequest):
    try:
        job_analysis = analyze_job(data.job_description)
        match_result = calculate_match(data.resume_analysis, job_analysis)
        match_result["recommendations"] = generate_recommendations(match_result["missing_skills"])
        return match_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job matching failed: {e}")

    # ============================================================
# RESUME UPLOAD ENDPOINT (file upload + text extraction)
# ============================================================

@app.post("/upload-resume")
async def upload_resume_endpoint(file: UploadFile = File(...)):
    if not file.filename.endswith((".pdf", ".docx")):
        raise HTTPException(status_code=400, detail="Only PDF or DOCX files are supported.")

    try:
        resume_text = extract_resume_text(file.file, filename=file.filename)

        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="No readable text found in this resume.")

        return {"resume_text": resume_text}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not process the resume: {e}")

    