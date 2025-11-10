import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------
# Helper Functions
# --------------------------

def categorize_transaction(description):
    description = description.lower()
    if "grocery" in description:
        return "Food & Dining"
    elif "gas" in description or "station" in description:
        return "Transportation"
    elif "netflix" in description or "spotify" in description:
        return "Entertainment"
    elif "salary" in description or "deposit" in description:
        return "Income"
    else:
        return "Uncategorized"

# --------------------------
# Streamlit UI
# --------------------------

st.set_page_config(page_title="Transaction Categorization & Reporting", layout="centered")

st.title("💳 Transaction Categorization")
st.subheader("Categorize Transactions Automatically")

# Upload or use sample data
uploaded_file = st.file_uploader("Upload a CSV file with transactions", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.info("Using sample data for demo")
    data = {
        "Description": ["Grocery Store", "Gas Station", "Netflix Subscription", "Salary Deposit"],
        "Amount": [-85.30, -45.00, -15.99, 3200.00],
    }
    df = pd.DataFrame(data)

# Categorize
df["Category"] = df["Description"].apply(categorize_transaction)
df["Type"] = df["Amount"].apply(lambda x: "Expense" if x < 0 else "Income")

# Display Categorized Transactions
st.markdown("### 🧾 Transaction Categorization")
for _, row in df.iterrows():
    color = "red" if row["Amount"] < 0 else "green"
    st.markdown(
        f"**{row['Description']}** &nbsp;&nbsp;&nbsp; "
        f"<span style='color:{color};'>${abs(row['Amount']):,.2f}</span> &nbsp;&nbsp;&nbsp; "
        f"_{row['Category']}_",
        unsafe_allow_html=True
    )

# --------------------------
# Dashboard View
# --------------------------
st.markdown("---")
st.markdown("### 📊 Basic Dashboard View")

income = df[df["Type"] == "Income"]["Amount"].sum()
expenses = df[df["Type"] == "Expense"]["Amount"].sum() * -1
balance = income - expenses

col1, col2, col3 = st.columns(3)
col1.metric("Income", f"${income:,.2f}")
col2.metric("Expenses", f"${expenses:,.2f}")
col3.metric("Balance", f"${balance:,.2f}")

# Pie Chart for Spending by Category
expense_df = df[df["Type"] == "Expense"]
if not expense_df.empty:
    cat_summary = expense_df.groupby("Category")["Amount"].sum().abs()

    fig, ax = plt.subplots()
    colors = sns.color_palette("pastel")
    ax.pie(cat_summary, labels=cat_summary.index, autopct="%1.1f%%", colors=colors)
    st.pyplot(fig)
else:
    st.write("No expense data available for chart.")

# Summary Table
st.markdown("### 📋 Spending Summary by Category")
st.dataframe(expense_df.groupby("Category")["Amount"].sum().abs().reset_index())
