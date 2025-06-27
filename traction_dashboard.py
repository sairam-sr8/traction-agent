import streamlit as st
import json
from traction_agent import analyze_traction
import pandas as pd

st.set_page_config(page_title="Traction Agent Dashboard", layout="wide")
st.title("🚀 Traction Agent Dashboard")

st.markdown("""
Enter your startup ID and paste or upload your event data (as JSON list). The agent will analyze your traction metrics and display the results below.
""")

# Input form
with st.form("traction_form"):
    startup_id = st.text_input("Startup ID", "startup_123")
    event_data_input = st.text_area("Paste Event Data (JSON list)",
        '[{"event_type": "page_view", "timestamp": "2024-06-01T10:00:00", "referrer": "linkedin.com", "device_type": "mobile"}]',
        height=150)
    uploaded_file = st.file_uploader("Or upload event data as .json file", type=["json"])
    submitted = st.form_submit_button("Analyze Traction")

# Parse event data
events = []
if uploaded_file is not None:
    try:
        events = json.load(uploaded_file)
    except Exception as e:
        st.error(f"Error reading uploaded file: {e}")
elif event_data_input:
    try:
        events = json.loads(event_data_input)
    except Exception as e:
        st.error(f"Error parsing event data: {e}")

# Run analysis and display results
if submitted and events:
    with st.spinner("Analyzing traction metrics..."):
        result = analyze_traction(startup_id, events)

    st.header("Results")
    st.subheader("Key Metrics")
    metrics = [
        ("Total Views", result.get("total_views", 0)),
        ("Clicks", result.get("clicks", 0)),
        ("Pitch Downloads", result.get("pitch_downloads", 0)),
        ("Conversion Rate", result.get("conversion_rate", "0%")),
        ("Active Days", result.get("active_days", 0)),
        ("Data Status", result.get("data_status", "-")),
    ]
    st.table(metrics)

    st.subheader("Top Referrers")
    st.write(result.get("top_referrers", []))

    if result.get("alerts"):
        st.warning("\n".join(result["alerts"]))

    # Heatmap visualization
    st.subheader("Weekday Heatmap")
    heatmap_data = result.get("heatmap_data", {})
    if heatmap_data:
        heatmap_df = pd.DataFrame(list(heatmap_data.items()), columns=["Day", "Events"])
        st.bar_chart(heatmap_df.set_index("Day"))

    # Daily trend
    st.subheader("Daily Trend")
    daily_trend = result.get("daily_trend", {})
    if daily_trend:
        daily_df = pd.DataFrame(list(daily_trend.items()), columns=["Date", "Events"])
        daily_df["Date"] = pd.to_datetime(daily_df["Date"])
        daily_df = daily_df.sort_values("Date")
        st.line_chart(daily_df.set_index("Date"))

    # Weekly trend
    st.subheader("Weekly Trend")
    weekly_trend = result.get("weekly_trend", {})
    if weekly_trend:
        weekly_df = pd.DataFrame(list(weekly_trend.items()), columns=["Week", "Events"])
        st.bar_chart(weekly_df.set_index("Week"))

    st.subheader("Raw Output")
    st.json(result)

elif submitted and not events:
    st.error("No event data provided. Please paste or upload a valid JSON list of events.") 