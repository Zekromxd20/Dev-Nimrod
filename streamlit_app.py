import streamlit as st
import google.generativeai as genai
import json
import re

# 1. Setup
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash') 
    else:
        st.error("API Key missing in Secrets!")
except Exception as e:
    st.error(f"Setup Error: {e}")

st.set_page_config(page_title="Dev Nimrod | Multi-Lang Auditor", layout="wide")

st.title("🚀 Dev Nimrod")
st.markdown("#### *Multi-Language Agentic Code Auditor*")

col_lang, _ = st.columns([1, 2])
with col_lang:
    selected_lang = st.selectbox(
        "Select Programming Language:",
        ["python", "cpp", "java", "javascript", "c", "go", "rust"],
        index=0
    )

code_input = st.text_area(f"Paste your {selected_lang} code here:", height=250)

if st.button("Run Multi-Agent Audit"):
    if not code_input:
        st.warning("Please provide code first!")
    else:
        with st.spinner(f"Agents are auditing {selected_lang}..."):
            prompt = f"""
            Act as three expert agents (Security, Performance, Architecture).
            Refactor this {selected_lang} code.
            Return ONLY a JSON object with these exact keys: 
            "refactored", "security_audit", "performance_audit", "architecture_audit", "complexity_score".
            
            CODE:
            {code_input}
            """
            
            try:
                response = model.generate_content(prompt)
                raw_text = response.text
                
                # --- ROBUST PARSING LOGIC ---
                # This finds anything between the first '{' and the last '}'
                json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
                
                if json_match:
                    json_str = json_match.group(0)
                    data = json.loads(json_str)
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"### 🛠️ Refactored {selected_lang.upper()}")
                        st.code(data['refactored'], language=selected_lang)
                        st.divider()
                        d_col1, d_col2 = st.columns(2)
                        with d_col1:
                            st.caption("Original")
                            st.code(code_input, language=selected_lang)
                        with d_col2:
                            st.caption("Refactored")
                            st.code(data['refactored'], language=selected_lang)

                    with col2:
                        st.write("### 🧠 Agent Findings")
                        st.info(f"**Complexity:** {data['complexity_score']}")
                        with st.expander("🛡️ Security", expanded=True): st.write(data['security_audit'])
                        with st.expander("⚡ Performance", expanded=True): st.write(data['performance_audit'])
                        with st.expander("🏗️ Architecture", expanded=True): st.write(data['architecture_audit'])
                else:
                    st.error("AI did not return valid JSON. Please try again.")
                    with st.expander("Show Raw Debug Info"):
                        st.write(raw_text)

            except Exception as e:
                st.error(f"Error: {str(e)}")
