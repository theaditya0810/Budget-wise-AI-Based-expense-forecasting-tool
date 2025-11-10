import streamlit as st
import pandas as pd
from datetime import datetime

TRANSACTION_FILE = "data/transactions.csv"

def transaction_page(user_email):
    st.subheader("💰 Transaction Input Interface")
    st.markdown("### Add New Transaction")

    date = st.date_input("Date", datetime.now())
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    desc = st.text_input("Description", placeholder="Transaction description")
    category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Other"])
    ttype = st.selectbox("Type", ["Expense", "Income"])

    if st.button("Add Transaction"):
        try:
            df = pd.read_csv(TRANSACTION_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=["email", "date", "amount", "desc", "category", "type"])

        new_txn = pd.DataFrame([[user_email, date, amount, desc, category, ttype]],
                               columns=df.columns)
        df = pd.concat([df, new_txn], ignore_index=True)
        df.to_csv(TRANSACTION_FILE, index=False)
        st.success("✅ Transaction added successfully!")

    st.markdown("### Your Transactions")
    try:
        df = pd.read_csv(TRANSACTION_FILE)
        user_txns = df[df["email"] == user_email]
        st.dataframe(user_txns)
    except FileNotFoundError:
        st.info("No transactions recorded yet.")
