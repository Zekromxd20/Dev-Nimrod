import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Dev Nimrod", page_icon="🏹", layout="wide")
st.title("🏹 Dev Nimrod: The Mighty Bug Hunter")

# Ensure the key is pulled from Streamlit Secrets
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Missing GOOGLE_API_KEY in Streamlit Secrets!")
else:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Use the most updated stable model name
    # If 2.0 fails, try 'gemini-1.5-flash' again or 'gemini-2.5-flash'
    model = genai.GenerativeModel('gemini-2.0-flash')

    code_input = st.text_area("📥 Paste your code here:", height=300)

    if st.button("🚀 Start the Hunt"):
        if not code_input:
            st.warning("Please paste some code first!")
        else:
            with st.spinner("Nimrod is tracking..."):
                try:
                    prompt = (
                        f"You are Dev Nimrod. Analyze this code for bugs. "
                        f"1. Hunter's Report: List the bugs. "
                        f"2. Smith's Fix: Full corrected code.\n\nCode:\n{code_input}"
                    )
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"The hunt hit a snag: {e}")
                    st.info("Try changing the model name to 'gemini-1.5-flash' in the code if this continues.")
