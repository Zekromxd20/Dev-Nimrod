import streamlit as st
import google.generativeai as genai
import json
import re

# 1. Setup with corrected Model Name
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # 'gemini-1.5-flash-latest' is the most stable endpoint name
        model = genai.GenerativeModel('gemini-1.5-flash-latest') 
    else:
        st.error("API Key missing in Secrets!")
except Exception as e:
    st.error(f"Setup Error: {e}")

st.set_page_config(page_title="Dev Nimrod | Multi-Agent Auditor", layout="wide")

# Sidebar for Language Selection - Looks more professional
with st.sidebar:
    st.title("⚙️ Settings")
    selected_lang = st.selectbox(
        "Target Language:",
        ["python", "cpp", "java", "javascript", "c", "go", "rust"],
        index=0
    )
    st.divider()
    st.info("Dev Nimrod uses 3 specialized agents to audit your code.")

st.title("🚀 Dev Nimrod")
st.markdown(f"#### *Agentic {selected_lang.capitalize()} Auditor*")

code_input = st.text_area(f"Paste your {selected_lang} code here:", height=300)

if st.button("Run Multi-Agent Audit"):
    if not code_input:
        st.warning("Please provide code first!")
    else:
        with st.spinner(f"Agents are analyzing {selected_lang} logic..."):
            # Refined prompt for better JSON consistency
            prompt = f"""
            Refactor this {selected_lang} code.
            Return ONLY a JSON object. No conversational text. 
            Keys: "refactored", "security_audit", "performance_audit", "architecture_audit", "complexity_score".
            
            CODE:
            {code_input}
            """
            
            try:
                response = model.generate_content(prompt)
                raw_text = response.text
                
                # Robust JSON extraction
                json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
                
                if json_match:
                    data = json.loads(json_match.group(0))
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.subheader(f"🛠️ Refactored {selected_lang.upper()}")
                        st.code(data['refactored'], language=selected_lang)
                        
                        st.divider()
                        st.subheader("🔍 Comparison")
                        d_col1, d_col2 = st.columns(2)
                        with d_col1:
                            st.caption("Original")
                            st.code(code_input, language=selected_lang)
                        with d_col2:
                            st.caption("Refactored")
                            st.code(data['refactored'], language=selected_lang)

                    with col2:
                        st.subheader("🧠 Agent Findings")
                        st.success(f"**Complexity:** {data['complexity_score']}")
                        
                        with st.expander("🛡️ Security Specialist", expanded=True):
                            st.write(data['security_audit'])
                        
                        with st.expander("⚡ Performance Engineer", expanded=True):
                            st.write(data['performance_audit'])
                            
                        with st.expander("🏗️ Clean Code Architect", expanded=True):
                            st.write(data['architecture_audit'])
                else:
                    st.error("AI returned an invalid format. Please try again.")

            except Exception as e:
                st.error(f"Execution Error: {str(e)}")
