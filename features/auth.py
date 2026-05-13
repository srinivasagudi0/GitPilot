import sqlite3
import bcrypt
import streamlit as st

db = "users.db"


def init_db():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    # will expand the fields as it gets better.
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    if result:
        stored_password = result[0]
        return bcrypt.checkpw(password.encode("utf-8"), stored_password)
    return False


# use this to say somwthing like wlcome back, username or welcome new user, username
def get_user_id(username):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    return None


def initialize_auth_state():
    init_db()
    if "authenticated_user" not in st.session_state:
        st.session_state.authenticated_user = None
    if "authenticated_user_id" not in st.session_state:
        st.session_state.authenticated_user_id = None

def require_login():
    initialize_auth_state()

    if st.session_state.authenticated_user:
        return

    st.title("GitPilot")
    st.write("Sign in to continue.")

    login_tab, signup_tab = st.tabs(["Log in", "Create account"])

    with login_tab:
        with st.form("login_form"):
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            submitted = st.form_submit_button("Log in")

        if submitted:
            if authenticate_user(username, password):
                st.session_state.authenticated_user = username
                st.session_state.authenticated_user_id = get_user_id(username)
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with signup_tab:
        with st.form("signup_form"):
            username = st.text_input("Username", key="signup_username")
            password = st.text_input("Password", type="password", key="signup_password")
            submitted = st.form_submit_button("Create account")

        if submitted:
            if not username or not password:
                st.warning("Enter a username and password.")
            elif register_user(username, password):
                st.session_state.authenticated_user = username
                st.session_state.authenticated_user_id = get_user_id(username)
                st.rerun()
            else:
                st.error("That username already exists.")

    st.stop()

def show_logout_button():
    st.sidebar.write(f"Signed in as **{st.session_state.authenticated_user}**")
    if st.sidebar.button("Log out"):
        st.session_state.authenticated_user = None
        st.session_state.authenticated_user_id = None
        st.rerun()
