
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

st.set_page_config(page_title='🧠 AI Recommendation Dashboard', layout='wide')

st.title("📊 AI-Powered Product Recommendation Dashboard")
st.markdown("This dashboard shows interaction logs, click-through rates, and engagement over time.")

# Connect to SQLite DB
conn = sqlite3.connect("recommendation_logs.db")
interaction_df = pd.read_sql("SELECT * FROM interactions", conn)
conn.close()

# Click-Through Rate (CTR) Chart
st.subheader("🔍 Click-Through Rate (CTR) per Product")
ctr = interaction_df.groupby('product_id')['reward'].mean().sort_values(ascending=False)
fig1, ax1 = plt.subplots(figsize=(10, 4))
ctr.plot(kind='bar', ax=ax1, color='skyblue')
ax1.set_xlabel("Product ID")
ax1.set_ylabel("CTR")
ax1.set_title("Click-Through Rate")
st.pyplot(fig1)

# Engagement Trend Over Time
st.subheader("⏱️ Engagement Over Time")
interaction_df['timestamp'] = pd.to_datetime(interaction_df['timestamp'])
interaction_df.set_index('timestamp', inplace=True)
engagement_trend = interaction_df.resample('1min')['reward'].mean()
fig2, ax2 = plt.subplots(figsize=(10, 4))
engagement_trend.plot(marker='o', linestyle='-', ax=ax2, color='green')
ax2.set_xlabel("Time")
ax2.set_ylabel("Avg Reward")
ax2.set_title("Engagement Trend")
st.pyplot(fig2)

# Data Download
st.subheader("📥 Download Logs")
st.download_button("Download as CSV", interaction_df.reset_index().to_csv(index=False), file_name="interaction_logs.csv", mime='text/csv')

st.success("Dashboard Ready! 🎉")
