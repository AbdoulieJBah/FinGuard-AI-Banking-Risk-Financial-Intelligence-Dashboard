import hashlib
import streamlit as st


USERS = {
    "admin@finguard.ai": {
        "name": "Admin User",
        "role": "Admin",
        "password": "admin123",
    },
    "executive@finguard.ai": {
        "name": "Executive User",
        "role": "Executive",
        "password": "executive123",
    },
    "risk@finguard.ai": {
        "name": "Risk Analyst",
        "role": "Risk Analyst",
        "password": "risk123",
    },
    "compliance@finguard.ai": {
        "name": "Compliance Officer",
        "role": "Compliance",
        "password": "compliance123",
    },
}


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def authenticate_user(email, password):
    email = email.strip().lower()

    if email not in USERS:
        return None

    user = USERS[email]

    if hash_password(password) == hash_password(user["password"]):
        return {
            "email": email,
            "name": user["name"],
            "role": user["role"],
            "status": "Active",
        }

    return None


def init_auth_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "user" not in st.session_state:
        st.session_state.user = None


def login_screen():
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }

    .login-card {
        max-width: 520px;
        margin: 80px auto 30px auto;
        padding: 38px;
        border-radius: 28px;
        background: rgba(15,23,42,0.92);
        border: 1px solid rgba(255,215,0,0.25);
        box-shadow: 0 18px 55px rgba(0,0,0,0.45);
        text-align: center;
    }

    .login-title {
        font-size: 2.4rem;
        font-weight: 950;
        color: #ffffff;
    }

    .login-title span {
        color: #facc15;
    }

    .login-subtitle {
        color: #d1d5db;
        margin-top: 8px;
        font-size: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-card">
        <div class="login-title">🏦 FinGuard <span>AI</span></div>
        <div class="login-subtitle">Secure Banking Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.2, 1.6, 1.2])

    with c2:
        st.subheader("Login")

        email = st.text_input("Email", placeholder="admin@finguard.ai")
        password = st.text_input("Password", type="password", placeholder="Enter password")

        if st.button("Login", use_container_width=True):
            user = authenticate_user(email, password)

            if user:
                st.session_state.authenticated = True
                st.session_state.user = user
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid email or password")

        with st.expander("Demo Users"):
            st.write("**Admin:** admin@finguard.ai / admin123")
            st.write("**Executive:** executive@finguard.ai / executive123")
            st.write("**Risk Analyst:** risk@finguard.ai / risk123")
            st.write("**Compliance:** compliance@finguard.ai / compliance123")


def require_login():
    init_auth_state()

    if not st.session_state.authenticated:
        login_screen()
        st.stop()


def logout_button():
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user = None
        st.rerun()


def get_current_user():
    init_auth_state()
    return st.session_state.user


def require_role(allowed_roles):
    require_login()

    user = get_current_user()

    if user is None:
        st.stop()

    if user["role"] not in allowed_roles and user["role"] != "Admin":
        st.error("You do not have permission to access this page.")
        st.stop()
