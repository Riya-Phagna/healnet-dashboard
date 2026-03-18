import streamlit as st

def show_notification(level, message):

    if level == "CRITICAL":
        st.error(f"🚨 CRITICAL ALERT: {message}")

    elif level == "WARNING":
        st.warning(f"⚠️ WARNING: {message}")

    else:
        st.success("✅ Patient Stable")
