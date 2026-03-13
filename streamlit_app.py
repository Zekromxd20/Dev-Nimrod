import streamlit as st
import google.generativeai as genai
import json

# 1. Setup - Using Streamlit Secrets
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash') 
    else:
        st.error("API Key not found in Secrets!")
except Exception as e:
    st.error(f"Setup Error: {e}")

st.set_page_config(page_title="Dev Nimrod | AI Code Auditor", layout="wide")

# Corrected CSS styling line
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stCodeBlock { border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Dev Nimrod")
st.markdown("#### *Agentic Multi-Agent Code Auditing & Refactoring*")

code_input = st.text_area("Paste your code here:", height=250)

if st.button("Run Multi-Agent Audit"):
    if not code_input:
        st.warning("Please provide code first!")
    else:
        with st.spinner("Agents are analyzing..."):
            prompt = f"""
            Act as a team of three expert agents: Security Specialist, Performance Engineer, and Clean Code Architect.
            Refactor the following code and return ONLY a JSON object with:
            "refactored": "code string",
            "security_audit": "finding",
            "performance_audit": "finding",
            "architecture_audit": "finding",
            "complexity_score": "score"
            
            CODE: {code_input}
            """
            
            try:
                response = model.generate_content(prompt)
                res_text = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(res_text)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write("### 🛠️ Refactored Output")
                    st.code(data['refactored'])
                    st.divider()
                    d_col1, d_col2 = st.columns(2)
                    with d_col1:
                        st.caption("Original")
                        st.code(code_input)
                    with d_col2:
                        st.caption("Refactored")
                        st.code(data['refactored'])

                with col2:
                    st.write("### 🧠 Agent Findings")
                    st.info(f"**Complexity:** {data['complexity_score']}")
                    with st.expander("🛡️ Security", expanded=True): st.write(data['security_audit'])
                    with st.expander("⚡ Performance", expanded=True): st.write(data['performance_audit'])
                    with st.expander("🏗️ Architecture", expanded=True): st.write(data['architecture_audit'])
            except Exception as e:
                st.error("The AI had a hiccup. Please try again!")
