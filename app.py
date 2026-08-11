import streamlit as st
from auth import show_auth_page
from api_client import (
    api_upload_resume,
    api_analyze_resume,
    api_search_jobs,
    api_match_job
)


# ============================================================
# PAGE CONFIG
# ============================================================
if "user" not in st.session_state:
    st.session_state.user = None

st.set_page_config(
    page_title="ResumeAI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Login status
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ============================================================
# GLOBAL LIGHT MODE (applies to login/signup page too)
# ============================================================

st.markdown("""
<style>
html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stSidebar"],
[data-testid="stBottomBlockContainer"] {
    background-color: #f8fafc !important;
    color: #0f172a !important;
}

/* Text elements */
h1, h2, h3, h4, h5, h6, p, span, label, div {
    color: #0f172a;
}

/* Tabs (Login / Sign Up) */
[data-testid="stTabs"] button {
    color: #64748b !important;
    background-color: transparent !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #0f172a !important;
}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
    background-color: #0f172a !important;
}

/* Form / card containers */
[data-testid="stForm"],
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 16px !important;
}

/* Text inputs and password fields */
[data-testid="stTextInput"] input,
[data-testid="stTextInput"] div[data-baseweb="input"] {
    background-color: #ffffff !important;
    color: #0f172a !important;
    border: 1px solid #cbd5e1 !important;
}
[data-testid="stTextInput"] label {
    color: #0f172a !important;
    font-weight: 500;
}
[data-testid="stTextInput"] input::placeholder {
    color: #94a3b8 !important;
}

/* Buttons */
div.stButton > button {
    background-color: #ffffff;
    color: #0f172a;
    border: 1px solid #cbd5e1;
}
div.stButton > button:hover {
    border-color: #0f172a;
    color: #0f172a;
}

/* Primary-style submit buttons (Login/Sign Up) */
button[kind="primary"], button[kind="primaryFormSubmit"] {
    background-color: #0f172a !important;
    color: #ffffff !important;
    border: none !important;
}

/* Divider lines */
hr, [data-testid="stDivider"] {
    border-color: #e2e8f0 !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOGIN / SIGNUP
# ============================================================

if not st.session_state.logged_in:

    show_auth_page()

else:

    # ============================================================
    # USER HEADER + LOGOUT
    # ============================================================

    user_name = st.session_state.user["name"] if st.session_state.user else "Guest"

    st.markdown(
        """
        <style>
        .st-key-user_header {
            background: white;
            border-bottom: 1px solid #e5e7eb;
            border-radius: 0 0 12px 12px;
            padding: 15px 25px;
            margin-bottom: 30px;
        }
        .st-key-user_header [data-testid="stHorizontalBlock"] {
            align-items: center;
        }
        .welcome-text {
            font-size: 20px;
            font-weight: 600;
            color: #111827;
        }
        .st-key-user_header div.stButton > button {
            width: auto;
            min-height: 38px;
            padding: 6px 18px;
            background: #ffffff;
            border: 1px solid #e5e7eb;
            color: #111827;
            font-size: 14px;
            font-weight: 600;
            border-radius: 8px;
            float: right;
        }
        .st-key-user_header div.stButton > button:hover {
            background: #f8fafc;
            border-color: #cbd5e1;
            color: #dc2626;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.container(key="user_header"):
        col1, col2 = st.columns([8, 1])

        with col1:
            st.markdown(
                f'<div class="welcome-text">Welcome, {user_name} 👋</div>',
                unsafe_allow_html=True
            )

        with col2:
            if st.button("Logout", key="logout_btn"):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.rerun()

    # ========================================================
    # EXISTING RESUME ANALYZER
    # ========================================================

    # Tumhara existing Hero Section,
    # Upload Section,
    # File Uploader,
    # Analyze button,
    # Feature Cards
    # yahan aayega.

    # ============================================================
    # CUSTOM CSS
    # ============================================================

    st.markdown("""
    <style>
    header[data-testid="stHeader"] {
    display: none;
    }

    .stApp {
    background-color: #f8fafc;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        padding-left: 5%;
        padding-right: 5%;
    }


    /* ================= HERO ================= */

    .hero {
        text-align: center;
        padding: 45px 20px 35px;
    }

    .hero-title {
        font-size: 48px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 12px;
    }

    .hero-subtitle {
        max-width: 750px;
        margin: auto;
        font-size: 19px;
        line-height: 1.6;
        color: #64748b;
    }


    /* ================= UPLOAD CARD ================= */

    .upload-card {
        background-color: #ffffff;
        padding: 32px;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
        margin-bottom: 20px;
    }

    .upload-title {
        font-size: 27px;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 10px;
    }

    .upload-description {
        font-size: 15px;
        line-height: 1.6;
        color: #64748b;
    }


    /* ================= FILE UPLOADER ================= */

    [data-testid="stFileUploader"] {
        background-color: #ffffff;
        border: 2px dashed #cbd5e1;
        border-radius: 16px;
        padding: 15px;
    }


    /* ================= SUCCESS BOX ================= */

    .success-box {
        background-color: #ecfdf5;
        border: 1px solid #a7f3d0;
        color: #065f46;
        padding: 13px 17px;
        border-radius: 10px;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    /* ================= EXPANDER ================= */

    [data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1;
        border-radius: 12px;
        overflow: hidden;
    }

    [data-testid="stExpander"] summary {
        background-color: #ffffff !important;
        color: #0f172a !important;
        font-weight: 600;
    }

    [data-testid="stExpander"] summary span,
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary svg {
        color: #0f172a !important;
        fill: #0f172a !important;
    }

    [data-testid="stExpander"] details[open] summary {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border-bottom: 1px solid #e2e8f0;
    }

    /* ================= EXTRACTED TEXT ================= */

    [data-testid="stExpanderDetails"],
    [data-testid="stExpanderDetails"] * {
        background-color: #f8fafc !important;
        color: #0f172a !important;
    }

    [data-testid="stExpanderDetails"] pre,
    [data-testid="stExpanderDetails"] code {
        font-size: 14px !important;
        line-height: 1.6 !important;
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
    }

    /* ================= FEATURE CARDS ================= */

    .feature-card {
        background-color: #ffffff;
        padding: 28px 20px;
        border-radius: 18px;
        border: 1px solid #e2e8f0;
        text-align: center;
        min-height: 165px;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
    }

    .feature-icon {
        font-size: 34px;
        margin-bottom: 10px;
    }

    .feature-title {
        font-size: 19px;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 8px;
    }

    .feature-description {
        font-size: 14px;
        line-height: 1.5;
        color: #64748b;
    }


    /* ================= BUTTON ================= */

    div.stButton > button {
        width: 100%;
        min-height: 50px;
        border-radius: 12px;
        font-size: 16px;
        font-weight: 600;
    }


    /* ================= TABLET ================= */

    @media (max-width: 992px) {

        .block-container {
            padding-left: 4%;
            padding-right: 4%;
        }

        .hero-title {
            font-size: 40px;
        }

        .hero-subtitle {
            font-size: 17px;
        }

        .upload-card {
            padding: 28px;
        }
    }


    /* ================= MOBILE ================= */

    @media (max-width: 768px) {

        .block-container {
            padding-top: 1rem;
            padding-left: 5%;
            padding-right: 5%;
        }

        .hero {
            padding: 30px 10px 25px;
        }

        .hero-title {
            font-size: 34px;
        }

        .hero-subtitle {
            font-size: 16px;
            line-height: 1.5;
        }

        .upload-card {
            padding: 22px;
            border-radius: 16px;
        }

        .upload-title {
            font-size: 22px;
        }

        .upload-description {
            font-size: 14px;
        }

        .feature-card {
            min-height: auto;
            padding: 22px 15px;
        }

        .feature-title {
            font-size: 17px;
        }

        .feature-description {
            font-size: 13px;
        }
    }


    /* ================= SMALL MOBILE ================= */

    @media (max-width: 480px) {

        .block-container {
            padding-left: 4%;
            padding-right: 4%;
        }

        .hero-title {
            font-size: 29px;
        }

        .hero-subtitle {
            font-size: 14px;
        }

        .upload-card {
            padding: 18px;
        }

        .upload-title {
            font-size: 20px;
        }

        .feature-card {
            padding: 20px 12px;
        }
    }

    </style>
    """, unsafe_allow_html=True)


    # ============================================================
    # HERO SECTION
    # ============================================================

    st.markdown("""
    <div class="hero">
    <div class="hero-title">📄 ResumeAI</div>
    <div class="hero-subtitle">AI-powered resume analysis to help you improve your profile and discover better job opportunities.</div>
    </div>
    """, unsafe_allow_html=True)


    # ============================================================
    # UPLOAD SECTION
    # ============================================================

    st.markdown("""
    <div class="upload-card">
    <div class="upload-title">📤 Upload Your Resume</div>
    <div class="upload-description">Upload your resume in PDF or DOCX format and let ResumeAI analyze your skills, experience and career profile.</div>
    </div>
    """, unsafe_allow_html=True)


    # ============================================================
    # FILE UPLOADER
    # ============================================================

    uploaded_file = st.file_uploader(
        "Choose your resume",
        type=["pdf", "docx"],
        label_visibility="collapsed"
    )


    # ============================================================
    # AFTER FILE UPLOAD
    # ============================================================

    if uploaded_file is not None:

        st.markdown(
            f"""
    <div class="success-box">✅ <strong>{uploaded_file.name}</strong> uploaded successfully!</div>
    """,
            unsafe_allow_html=True
        )

        analyze_button = st.button(
            "✨ Analyze My Resume",
            use_container_width=True
        )

        if analyze_button:
            resume_text = None
            with st.spinner("Reading your resume..."):
                resume_text, error = api_upload_resume(uploaded_file)
                if error:
                    st.error(error)
                    st.session_state.resume_text = None
                else:
                    st.session_state.resume_text = resume_text

            if resume_text and resume_text.strip():
                with st.spinner("Analyzing your resume with AI..."):
                    analysis = api_analyze_resume(resume_text)
                    st.session_state.resume_analysis = analysis
    # ============================================================
    # SHOW ANALYSIS RESULTS (persists across reruns)
    # ============================================================

    if st.session_state.get("resume_text"):

        resume_text = st.session_state.resume_text

        if resume_text.strip():
            st.success("Resume text extracted successfully!")

            # with st.expander("View Extracted Resume Text"):
            #     st.text(resume_text)

            # ================================================
            # RESUME ANALYSIS DISPLAY
            # ================================================
            analysis = st.session_state.get("resume_analysis", {})

            if analysis:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### 🧠 AI Resume Analysis")

                acol1, acol2 = st.columns(2)

                with acol1:
                    st.markdown("**Skills**")
                    skills_all = analysis.get("skills", []) + analysis.get("programming_languages", []) + analysis.get("frameworks", [])
                    st.write(", ".join(skills_all) or "Not found")

                    st.markdown("**Tools**")
                    st.write(", ".join(analysis.get("tools", [])) or "Not found")

                    st.markdown("**Education**")
                    st.write(", ".join(analysis.get("education", [])) or "Not found")

                with acol2:
                    st.markdown("**Possible Roles**")
                    st.write(", ".join(analysis.get("possible_roles", [])) or "Not found")

                    st.markdown("**Domains**")
                    st.write(", ".join(analysis.get("domains", [])) or "Not found")

                    st.markdown("**Projects**")
                    for proj in analysis.get("projects", []):
                        st.write(f"• {proj}")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 💼 Find Matching Jobs")

            suggested_role = analysis.get("possible_roles", [""])[0] if analysis.get("possible_roles") else ""

            job_query = st.text_input(
                "Enter job role to search",
                value=suggested_role,
                placeholder="e.g. Python Developer, Data Analyst"
            )

            search_button = st.button("🔍 Search Jobs", use_container_width=True)

            if "job_results" not in st.session_state:
                st.session_state.job_results = []
            if "jobs_page" not in st.session_state:
                st.session_state.jobs_page = 1
            if "job_matches" not in st.session_state:
                st.session_state.job_matches = {}
            if "last_query" not in st.session_state:
                st.session_state.last_query = ""

            if search_button:
                if job_query.strip() == "":
                    st.warning("Please enter a job role to search.")
                else:
                    with st.spinner("Fetching real job listings..."):
                        new_jobs = api_search_jobs(query=job_query, location="india", page=1)

                    st.session_state.job_results = new_jobs
                    st.session_state.jobs_page = 1
                    st.session_state.last_query = job_query
                    st.session_state.job_matches = {}

                    if not new_jobs:
                        st.info("No jobs found. Try a different keyword.")

            # ================================================
            # DISPLAY JOBS (basic info, match computed on click)
            # ================================================

            if st.session_state.job_results:
                st.success(f"Found {len(st.session_state.job_results)} jobs for '{st.session_state.last_query}'")

                for idx, job in enumerate(st.session_state.job_results):
                    job_key = job['job_url']

                    with st.container(border=True):
                        st.markdown(f"**{job['title']}**")
                        st.markdown(f"🏢 {job['company']}  |  📍 {job['location']}")
                        st.markdown(f"🕒 Posted: {job['date_posted'][:10]}")

                        with st.expander("View Job Description"):
                            st.write(job['description'])

                        check_match_col, apply_col = st.columns(2)

                        with check_match_col:
                            check_button = st.button(
                                "🎯 Check Match Score",
                                key=f"check_{idx}",
                                use_container_width=True
                            )

                        with apply_col:
                            st.link_button("Apply Now →", job['job_url'], use_container_width=True)

                        if check_button:
                            with st.spinner("Analyzing match..."):
                                match_result = api_match_job(analysis, job['description'])
                                if match_result:
                                    st.session_state.job_matches[job_key] = match_result
                                else:
                                    st.error("Match analysis failed. Please try again.")

                        if job_key in st.session_state.job_matches:
                            match = st.session_state.job_matches[job_key]

                            st.markdown("---")

                            if match.get("insufficient_data"):
                                st.warning("⚠️ This job's description is too short/generic to calculate an accurate match. Check 'Apply Now' to view the full posting.")
                            else:
                                st.metric("Match Score", f"{match['match_percentage']}%")
                                st.progress(match['match_percentage'] / 100)

                            mcol1, mcol2 = st.columns(2)

                            with mcol1:
                                st.markdown("**✓ Matched Skills**")
                                if match['matched_skills']:
                                    for s in match['matched_skills']:
                                        st.markdown(f"- {s.title()}")
                                else:
                                    st.write("None found")

                            with mcol2:
                                st.markdown("**✗ Missing Skills**")
                                if match['missing_skills']:
                                    for s in match['missing_skills']:
                                        st.markdown(f"- {s.title()}")
                                else:
                                    st.write("None — great match!")

                            if match['recommendations']:
                                with st.expander("💡 Improvement Suggestions"):
                                    for rec in match['recommendations']:
                                        st.markdown(f"**{rec['skill']}**: {rec['suggestion']}")

                load_more = st.button("⬇️ Load More Jobs", use_container_width=True)

                if load_more:
                    next_page = st.session_state.jobs_page + 1
                    with st.spinner("Fetching more jobs..."):
                        more_jobs = api_search_jobs(
                            query=st.session_state.last_query,
                            location="india",
                            page=next_page
                        )

                    if more_jobs:
                        st.session_state.job_results.extend(more_jobs)
                        st.session_state.jobs_page = next_page
                        st.rerun()
                    else:
                        st.info("No more jobs found.")

        else:
            st.warning("No readable text was found in this resume.")

    # ============================================================
    # FEATURE CARDS
    # ============================================================

    # ============================================================
    # FEATURE CARDS
    # ============================================================

    if not st.session_state.get("resume_analysis"):

        st.markdown("<br>", unsafe_allow_html=True)

        fcol1, fcol2, fcol3 = st.columns(3)


        # ---------------- CARD 1 ----------------

        with fcol1:

            st.markdown("""
        <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Resume Score</div>
        <div class="feature-description">Get an AI-powered evaluation of your resume quality and overall profile.</div>
        </div>
        """, unsafe_allow_html=True)


        # ---------------- CARD 2 ----------------

        with fcol2:

            st.markdown("""
        <div class="feature-card">
        <div class="feature-icon">🎯</div>
        <div class="feature-title">Skill Analysis</div>
        <div class="feature-description">Discover your strengths, missing skills and areas that need improvement.</div>
        </div>
        """, unsafe_allow_html=True)


        # ---------------- CARD 3 ----------------

        with fcol3:

            st.markdown("""
        <div class="feature-card">
        <div class="feature-icon">💼</div>
        <div class="feature-title">Job Matching</div>
        <div class="feature-description">Find relevant jobs and understand how well your profile matches each opportunity.</div>
        </div>
        """, unsafe_allow_html=True)