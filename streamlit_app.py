import streamlit as st
import google.generativeai as genai
import os

# Page Config
st.set_page_config(page_title="Dev Nimrod", page_icon="🏹", layout="wide")

st.title("🏹 Dev Nimrod: The Mighty Bug Hunter")
st.markdown("*Agentic AI Bug Detection (Free Tier)*")

# Access Secret Key (We will set this in Step 3)
api_key = st.secrets["GOOGLE_API_KEY"]

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    code_input = st.text_area("📥 Paste your code here:", height=300)

    if st.button("🚀 Start the Hunt"):
        if not code_input:
            st.warning("Please paste some code first!")
        else:
            with st.spinner("Nimrod is tracking..."):
                # Agentic prompt logic
                prompt = (
                    f"You are Dev Nimrod. Analyze this code for bugs and logic flaws. "
                    f"First, provide a 'Hunter's Report' listing the bugs. "
                    f"Second, provide a 'Smith's Fix' with the complete corrected code.\n\n"
                    f"Code:\n{code_input}"
                )
                response = model.generate_content(prompt)
                st.markdown(response.text)
else:
    st.error("API Key not found. Please check Streamlit Secrets.")
