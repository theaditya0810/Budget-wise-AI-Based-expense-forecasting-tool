import streamlit as st

def profile_page(user_email):
    st.subheader("👤 Profile Management")
    st.write(f"**Logged in as:** {user_email}")
    name = st.text_input("Full Name", placeholder="Enter your full name")
    phone = st.text_input("Phone Number", placeholder="Enter your phone number")
    bio = st.text_area("Bio", placeholder="Write something about yourself")

    if st.button("Update Profile"):
        st.success("Profile updated successfully!")
