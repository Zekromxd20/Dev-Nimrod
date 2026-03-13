import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dev Nimrod", page_icon="🏹", layout="wide")

st.title("🏹 Dev Nimrod: The Mighty Bug Hunter")
st.markdown("### Agentic AI Bug Detection & Code Refactoring")

# --- API KEY SETUP ---
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Missing GOOGLE_API_KEY in Streamlit Secrets! Check your Settings.")
else:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # --- MODEL SELECTION ---
    # We use 'gemini-3-flash-preview' as it's the current free-tier workhorse in 2026.
    # Failover model: 'gemini-3.1-flash-lite-preview'
    model_id = "gemini-3-flash-preview"
    
    try:
        model = genai.GenerativeModel(model_id)
    except Exception:
        model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

    # --- UI LAYOUT ---
    code_input = st.text_area("📥 Paste your code here:", height=300, placeholder="#include <stdio.h> ...")

    if st.button("🚀 Start the Hunt"):
        if not code_input:
            st.warning("Please paste some code first!")
        else:
            with st.spinner("Nimrod is tracking the scent..."):
                try:
                    # Multi-agent style instructions
                    prompt = (
                        f"You are Dev Nimrod. Analyze this code for bugs and logic flaws.\n"
                        f"1. Hunter's Report: List the bugs clearly with line references.\n"
                        f"2. Smith's Fix: Provide the full, corrected code block.\n\n"
                        f"Code:\n{code_input}"
                    )
                    
                    response = model.generate_content(prompt)
                    st.success(f"🎯 Hunt Successful! (Model: {model_id})")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"The hunt hit a snag: {e}")
                    st.info("Check if your API key is correct in the Streamlit Cloud secrets.")
