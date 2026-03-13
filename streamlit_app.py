import streamlit as st
import google.generativeai as genai
import json

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

# --- NEW: Language Selection ---
col_lang, col_empty = st.columns([1, 2])
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
        with st.spinner(f"Analyzing {selected_lang} logic..."):
            # The prompt now includes the selected language
            prompt = f"""
            Act as a team of three expert agents specializing in {selected_lang}.
            Refactor the following {selected_lang} code and return ONLY a JSON object with:
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
                    st.write(f"### 🛠️ Refactored {selected_lang.upper()}")
                    # Updated to use the dynamic language variable
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
            except:
                st.error("AI parsing error. Try again!")
