import streamlit as st
import google.generativeai as genai
import json
from streamlit_diff_viewer import diff_viewer

# 1. Setup - Using Streamlit Secrets for the API Key
# Go to Streamlit Cloud Settings > Secrets to add: GOOGLE_API_KEY = "your_key"
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash') # Using Flash for speed/hackathons
except Exception as e:
    st.error("API Key not found. Please add GOOGLE_API_KEY to Streamlit Secrets.")

st.set_page_config(page_title="Dev Nimrod | AI Code Auditor", layout="wide")

st.title("🚀 Dev Nimrod")
st.markdown("### *Agentic Code Auditing & Intelligent Refactoring*")

# Sidebar for metrics
st.sidebar.header("Agent Stats")
st.sidebar.info("Model: Gemini 3 Flash")

# Input area
code_input = st.text_area("Paste code to audit:", height=250, placeholder="Enter Python, C++, or JS code...")

if st.button("Run Audit & Refactor"):
    if not code_input:
        st.warning("Please provide code first!")
    else:
        with st.spinner("Nimrod is analyzing..."):
            # Prompt forces JSON for structured "Why" and "Code"
            prompt = f"""
            Refactor this code. Return ONLY a JSON object:
            {{
                "refactored": "string",
                "reasoning": ["list of strings"],
                "complexity": "string"
            }}
            CODE: {code_input}
            """
            
            response = model.generate_content(prompt)
            
            try:
                # Cleaning the AI output to ensure valid JSON
                res_text = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(res_text)
                
                # Layout for results
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.success(f"**Complexity:** {data['complexity']}")
                    st.write("#### Why Refactor?")
                    for r in data['reasoning']:
                        st.write(f"- {r}")
                
                with col2:
                    st.write("#### Refactored Output")
                    st.code(data['refactored'], language='python')

                st.divider()
                st.write("#### 🔍 Visual Diff (Old vs New)")
                diff_viewer(old_text=code_input, new_text=data['refactored'], lang="python")
                
            except:
                st.error("Failed to parse AI response. Try clicking refactor again.")
