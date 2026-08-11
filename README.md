# 📄 ResumeAI — AI-Powered Resume Analyzer & Job Matcher

ResumeAI is a full-stack web application that helps job seekers analyze their resumes using AI and discover real, relevant job opportunities matched to their skill profile — with an explainable match score, missing-skill breakdown, and personalized improvement suggestions.

---

## ✨ Features

- 🔐 **Secure Authentication** — Signup/login with bcrypt password hashing
- 📄 **Resume Upload & Parsing** — Supports PDF and DOCX formats
- 🧠 **AI Resume Analysis** — Uses Google Gemini to extract skills, programming languages, frameworks, tools, education, projects, certifications, and suggested job roles
- 💼 **Real-Time Job Search** — Aggregates live job listings from **Adzuna** and **Jooble** APIs
- 🎯 **On-Demand Match Scoring** — Click any job to calculate a skill-based match percentage between the resume and that specific job description
- ✅ **Matched vs. Missing Skills** — Clear breakdown of what matches and what's missing
- 💡 **Personalized Recommendations** — Actionable suggestions for each missing skill
- 🔗 **Apply Now** — Always available, regardless of match score — direct link to the original job posting
- ⬇️ **Load More Jobs** — Paginated job browsing

---

## 🛠️ Tech Stack

| Layer          | Technology                          |
|----------------|--------------------------------------|
| Frontend       | Streamlit                           |
| Backend        | FastAPI                             |
| Database       | SQLite                              |
| AI / LLM       | Google Gemini API                   |
| Job Data       | Adzuna API, Jooble API              |
| Auth           | bcrypt password hashing             |
| File Parsing   | PyPDF2, python-docx                 |

---

## 🏗️ Architecture

```
┌─────────────────────┐
│  Streamlit Frontend  │   (UI, session state, user interaction)
└──────────┬───────────┘
           │  HTTP requests (REST API)
           ▼
┌─────────────────────┐
│   FastAPI Backend    │   (business logic, validation)
└──────────┬───────────┘
           │
   ┌───────┼────────────────────┬──────────────────────┐
   ▼                            ▼                       ▼
┌─────────┐          ┌────────────────────┐   ┌──────────────────┐
│ SQLite  │          │  Google Gemini API  │   │ Adzuna + Jooble   │
│ (Users) │          │ (Resume/Job Analysis)│   │  (Job Listings)   │
└─────────┘          └────────────────────┘   └──────────────────┘
```

The Streamlit frontend never talks to the database or external APIs directly — every action goes through the FastAPI backend, which keeps business logic centralized and reusable (e.g. for a future mobile app or different frontend).

---

## 📂 Project Structure

```
ai-resume-analyzer/
│
├── app.py                  # Streamlit frontend
├── main.py                 # FastAPI backend entry point
├── api_client.py           # Streamlit → FastAPI request wrapper
│
├── auth.py                 # Login/signup UI (Streamlit)
├── database.py             # SQLite user table + auth logic
│
├── resume_parser.py        # PDF/DOCX text extraction
├── resume_analyzer.py      # Gemini-based resume analysis
│
├── job_api.py               # Adzuna + Jooble job fetching
├── job_analyzer.py         # Gemini-based job description analysis
├── job_matcher.py          # Resume vs. job skill matching logic
├── recommendations.py      # Missing-skill improvement suggestions
│
├── requirements.txt
├── .gitignore
└── .env                    # API keys (not committed)
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- API keys for:
  - [Google Gemini](https://aistudio.google.com/apikey)
  - [Adzuna](https://developer.adzuna.com/)
  - [Jooble](https://jooble.org/api/about)

### Installation

```bash
git clone https://github.com/nitimishra/ai-resume-analyzer.git
cd ai-resume-analyzer

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_key_here
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key
JOOBLE_API_KEY=your_jooble_key_here
```

### Running Locally

Two servers need to run at the same time, in **separate terminals**:

**Terminal 1 — Backend:**
```bash
uvicorn main:app --reload --port 8080
```

**Terminal 2 — Frontend:**
```bash
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

Backend API docs (Swagger UI) are available at **http://localhost:8080/docs**.

---

## 🔌 API Endpoints (FastAPI Backend)

| Method | Endpoint          | Description                                  |
|--------|--------------------|-----------------------------------------------|
| POST   | `/signup`          | Create a new user account                    |
| POST   | `/login`           | Authenticate a user                          |
| POST   | `/upload-resume`   | Upload PDF/DOCX and extract text             |
| POST   | `/analyze-resume`  | AI-analyze resume text into structured data  |
| POST   | `/jobs`            | Search jobs (Adzuna + Jooble combined)       |
| POST   | `/match-job`       | Compute match score between resume and job   |

---

## 🧭 How It Works

1. User signs up / logs in
2. Uploads a resume (PDF or DOCX)
3. Gemini AI extracts structured data — skills, tools, education, projects, and suggested roles
4. App searches live jobs matching the suggested role (or any custom query)
5. User browses job listings — clicking **"Check Match Score"** on any job triggers an on-demand AI analysis of that job description
6. The app compares resume skills against job requirements and shows:
   - Match percentage
   - Matched skills ✓
   - Missing skills ✗
   - Personalized suggestions for each missing skill
7. **Apply Now** is always available — a low match score never blocks applying

---

## 📌 Notes

- Job data is sourced from third-party aggregators (Adzuna, Jooble); descriptions are sometimes truncated at the source.
- This project was built as an internship/academic project to demonstrate full-stack development with AI integration (Streamlit + FastAPI + LLM + external APIs).

---

## 👩‍💻 Author

**Niti Mishra**
B.Tech Computer Science, AKTU
[GitHub](https://github.com/nitimishra)
