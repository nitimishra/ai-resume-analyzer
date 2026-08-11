import streamlit as st
from api_client import api_signup, api_login


def show_auth_page():

    # =========================
    # CUSTOM CSS
    # =========================

    st.markdown("""
    <style>

    .block-container {
        padding-top: 4rem;
    }

    div[data-testid="stForm"] {
        background: #171a23;
        border: 1px solid #363a48;
        border-radius: 16px;
        padding: 28px;
        max-width: 520px;
        margin: auto;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 45px;
        font-weight: 600;
    }

    </style>
    """, unsafe_allow_html=True)


    # =========================
    # CENTER CARD
    # =========================

    left, center, right = st.columns([1, 2, 1])

    with center:

        st.markdown(
            """
            <div style="text-align:center;">
                <h1>📄 AI Resume Analyzer</h1>
                <p style="color:#9ca3af;">
                    AI-powered resume analysis and job matching
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        login_tab, signup_tab = st.tabs(["Login", "Sign Up"])


        # =====================================================
        # LOGIN
        # =====================================================

        with login_tab:

            with st.form("login_form"):

                st.subheader("Login to your account")

                email = st.text_input(
                    "Email",
                    placeholder="Enter your email"
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password"
                )

                login_button = st.form_submit_button(
                    "Login",
                    use_container_width=True
                )

            if login_button:

                if not email or not password:

                    st.warning(
                        "Please enter email and password."
                    )

                else:

                    user = api_login(email, password)

                    if user:

                        st.session_state.logged_in = True
                        st.session_state.user = user

                        st.rerun()

                    else:

                        st.error(
                            "Invalid email or password."
                        )


        # =====================================================
        # SIGN UP
        # =====================================================

        with signup_tab:

            with st.form("signup_form"):

                st.subheader("Create your account")

                name = st.text_input(
                    "Full Name",
                    placeholder="Enter your name"
                )

                email = st.text_input(
                    "Email",
                    placeholder="Enter your email"
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Create a password"
                )

                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Confirm your password"
                )

                signup_button = st.form_submit_button(
                    "Create Account",
                    use_container_width=True
                )

            if signup_button:

                if not name or not email or not password:

                    st.warning(
                        "Please fill all fields."
                    )

                elif password != confirm_password:

                    st.error(
                        "Passwords do not match."
                    )

                elif len(password) < 6:

                    st.warning(
                        "Password must contain at least 6 characters."
                    )

                else:

                    success, message = api_signup(
                        name,
                        email,
                        password
                    )

                    if success:

                        st.success(message)
                        st.info("You can now login.")

                    else:

                        st.error(message)


        # =========================
        # FOOTER
        # =========================

        st.markdown(
            """
            <div style="
                text-align:center;
                margin-top:25px;
                color:#9ca3af;
                font-size:14px;
            ">
                📄 <b>ResumeAI</b><br>
                AI-powered resume analysis to help you improve your profile
            </div>
            """,
            unsafe_allow_html=True
        )