import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dev Nimrod", page_icon="🏹", layout="wide")

st.title("🏹 Dev Nimrod: The Mighty Bug Hunter")
st.markdown("### Agentic AI Bug Detection & Code Refactoring")

# --- API KEY & MODEL SETUP ---
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Missing GOOGLE_API_KEY in Streamlit Secrets! Check your Settings.")
else:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # gemini-3-flash is the current 2026 stable model for free usage
    model = genai.GenerativeModel('gemini-3-flash')

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
                        f"You are Dev Nimrod. First, act as a 'Bug Hunter' and list the errors in this code. "
                        f"Second, act as a 'Master Smith' and provide the full corrected code.\n\n"
                        f"Code:\n{code_input}"
                    )
                    
                    response = model.generate_content(prompt)
                    st.success("🎯 Hunt Successful!")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"The hunt hit a snag: {e}")
                    st.info("Tip: If you see a 404, the model name might have updated. Try 'gemini-3-flash-preview'.")
