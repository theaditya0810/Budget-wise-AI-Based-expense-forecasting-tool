import streamlit as st
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly
import plotly.graph_objects as go
from datetime import datetime

# ----------------- PAGE CONFIG -----------------
st.set_page_config(page_title="Budgetwise Forecast", page_icon="💰", layout="wide")

# ----------------- HEADER -----------------
st.title("💰 Expense Forecast & Goal Setting")
st.markdown("### Powered by Prophet Forecasting Engine")

st.sidebar.header("Upload & Settings")
uploaded_file = st.sidebar.file_uploader("📁 Upload Transaction Data (CSV)", type=["csv"])

# ----------------- LOAD DATA -----------------
if uploaded_file:
    data = pd.read_csv(uploaded_file)
else:
    data = pd.read_csv("data/sample_expenses.csv")

# Convert and prepare data
data['Date'] = pd.to_datetime(data['Date'])
data = data.sort_values('Date')

# ----------------- UI FILTERS -----------------
st.sidebar.markdown("---")
category_options = ['All Categories'] + list(data['Category'].unique())
selected_category = st.sidebar.selectbox("📊 Select Category", category_options)

freq_option = st.sidebar.selectbox("📅 Frequency", ['Monthly', 'Weekly'])

# ----------------- DATA AGGREGATION -----------------
if selected_category != 'All Categories':
    filtered = data[data['Category'] == selected_category]
else:
    filtered = data.copy()

# Aggregate by frequency
if freq_option == 'Monthly':
    df_agg = filtered.groupby(pd.Grouper(key='Date', freq='M'))['Amount'].sum().reset_index()
else:
    df_agg = filtered.groupby(pd.Grouper(key='Date', freq='W'))['Amount'].sum().reset_index()

df_agg = df_agg.rename(columns={'Date': 'ds', 'Amount': 'y'})

# ----------------- PROPHET MODEL -----------------
model = Prophet()
model.fit(df_agg)

future = model.make_future_dataframe(periods=3, freq='M' if freq_option == 'Monthly' else 'W')
forecast = model.predict(future)

# ----------------- PLOT -----------------
fig = go.Figure()

# Actual historical
fig.add_trace(go.Scatter(
    x=df_agg['ds'],
    y=df_agg['y'],
    mode='lines+markers',
    name='Historical Expenses',
    line=dict(color='#007bff', width=2)
))

# Forecasted mean
fig.add_trace(go.Scatter(
    x=forecast['ds'],
    y=forecast['yhat'],
    mode='lines+markers',
    name='Forecast',
    line=dict(color='#00cc96', dash='dot')
))

# Confidence interval
fig.add_trace(go.Scatter(
    x=list(forecast['ds']) + list(forecast['ds'])[::-1],
    y=list(forecast['yhat_upper']) + list(forecast['yhat_lower'])[::-1],
    fill='toself',
    fillcolor='rgba(0,204,150,0.1)',
    line=dict(color='rgba(255,255,255,0)'),
    hoverinfo="skip",
    name='Confidence Interval'
))

fig.update_layout(
    title="📈 Prophet Forecast Visualization",
    xaxis_title="Date",
    yaxis_title="Expense Amount ($)",
    template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# ----------------- METRICS -----------------
col1, col2, col3 = st.columns(3)
current_month = df_agg['y'].iloc[-1]
next_forecast = forecast['yhat'].iloc[-1]
confidence = round(100 - abs(forecast['yhat_upper'].iloc[-1] - forecast['yhat_lower'].iloc[-1]) / forecast['yhat_upper'].iloc[-1] * 100, 2)

col1.metric("Current Monthly", f"${current_month:,.0f}")
col2.metric("Next Month Forecast", f"${next_forecast:,.0f}")
col3.metric("Confidence", f"{confidence}%")

# ----------------- GOAL SETTING -----------------
st.markdown("### 🎯 Set Your Financial Goals")
goal_type = st.selectbox("Goal Type", ["Save More", "Reduce Spending"])
goal_amount = st.number_input("Enter target amount ($):", min_value=0, value=500)
goal_date = st.date_input("Target Date", datetime.now())

st.success(f"Goal set successfully: **{goal_type} ${goal_amount} by {goal_date}**")

# ----------------- DISPLAY CHART -----------------
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("Developed as part of Forecasting Engine & Goal Setting Module using Streamlit and Prophet.")
