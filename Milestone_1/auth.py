import streamlit as st
import pandas as pd
from utils import hash_password, check_password, create_jwt_token

USER_FILE = "data/users.csv"

def register_user():
    st.subheader("📝 Create Account")
    email = st.text_input("Email", placeholder="your@email.com")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if password != confirm:
            st.error("Passwords do not match.")
            return
        try:
            users = pd.read_csv(USER_FILE)
        except FileNotFoundError:
            users = pd.DataFrame(columns=["email", "password"])

        if email in users["email"].values:
            st.warning("User already exists.")
        else:
            users.loc[len(users)] = [email, hash_password(password)]
            users.to_csv(USER_FILE, index=False)
            st.success("✅ Registration successful! Please log in.")


def login_user():
    st.subheader("🔐 Sign In to Budget Tracker")
    email = st.text_input("Email", placeholder="your@email.com")
    password = st.text_input("Password", type="password")

    if st.button("Sign In"):
        try:
            users = pd.read_csv(USER_FILE)
        except FileNotFoundError:
            st.error("No users registered yet.")
            return

        user = users[users["email"] == email]
        if not user.empty and check_password(password, user.iloc[0]["password"]):
            token = create_jwt_token(email)
            st.session_state["token"] = token
            st.success("🎉 Login successful!")
            st.rerun()
        else:
            st.error("Invalid email or password.")
