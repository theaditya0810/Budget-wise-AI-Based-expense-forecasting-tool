import streamlit as st
from auth import login_user, register_user
from profile import profile_page
from transaction import transaction_page
from utils import verify_jwt_token

st.set_page_config(page_title="Budget Tracker", layout="centered")

st.markdown("<h2 style='text-align:center; color:#1B7CC7;'>💼 Budget Tracker</h2>", unsafe_allow_html=True)
st.divider()

if "token" not in st.session_state:
    menu = st.sidebar.radio("Menu", ["Login", "Register"])
    if menu == "Login":
        login_user()
    else:
        register_user()
else:
    token_data = verify_jwt_token(st.session_state["token"])
    if token_data:
        email = token_data["email"]
        choice = st.sidebar.radio("Navigation", ["Profile", "Transactions", "Logout"])

        if choice == "Profile":
            profile_page(email)
        elif choice == "Transactions":
            transaction_page(email)
        elif choice == "Logout":
            st.session_state.clear()
            st.rerun()
    else:
        st.error("Session expired. Please log in again.")
        st.session_state.clear()
