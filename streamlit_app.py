import streamlit as st
import google.generativeai as genai
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dev Nimrod", page_icon="🏹", layout="wide")

st.title("🏹 Dev Nimrod: The Mighty Bug Hunter")
st.markdown("### Agentic AI Bug Detection & Code Refactoring")

# --- API KEY CHECK ---
# Ensure "GOOGLE_API_KEY" is set in your Streamlit Cloud Secrets
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Missing GOOGLE_API_KEY in Streamlit Secrets! Go to Settings > Secrets to add it.")
else:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Using the most stable stable alias for the free tier in 2026
    model = genai.GenerativeModel('gemini-3-flash')

    # --- UI LAYOUT ---
    code_input = st.text_area("📥 Paste your code here:", height=300, placeholder="int main() { ... }")

    if st.button("🚀 Start the Hunt"):
        if not code_input:
            st.warning("Nimrod needs some scent! Please paste code first.")
        else:
            with st.spinner("Nimrod is tracking the bugs..."):
                try:
                    # Agentic instructions for the "Hunter" and "Smith"
                    prompt = (
                        f"You are Dev Nimrod. Analyze this code for bugs and logic flaws.\n"
                        f"1. Hunter's Report: List the bugs clearly with line references.\n"
                        f"2. Smith's Fix: Provide the full, corrected code block.\n\n"
                        f"Code to analyze:\n{code_input}"
                    )
                    
                    response = model.generate_content(prompt)
                    
                    # Display the results
                    st.success("🎯 Hunt Successful!")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"The hunt hit a snag: {e}")
                    st.info("Tip: If you see a 429 error, wait 60 seconds. The free tier has a rate limit!")
