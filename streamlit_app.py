import streamlit as st
import google.generativeai as genai
import json
import re

# 1. Setup - Updated to the 2026 Stable Model
MODEL_NAME = 'gemini-2.5-flash' # The current stable workhorse

try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel(MODEL_NAME) 
    else:
        st.error("API Key missing! Go to 'Manage app' > 'Settings' > 'Secrets' and add GOOGLE_API_KEY.")
except Exception as e:
    st.error(f"Setup Error: {e}")

st.set_page_config(page_title="Dev Nimrod | Agentic Auditor", layout="wide")

# Sidebar for Language Selection
with st.sidebar:
    st.title("⚙️ Dev Nimrod Settings")
    st.markdown("---")
    selected_lang = st.selectbox(
        "Programming Language:",
        ["python", "cpp", "java", "javascript", "c", "go", "rust"],
        index=0
    )
    st.divider()
    st.info("🎯 **Strategy:** Multi-Agent specialized auditing (Security, Performance, Architecture).")

st.title("🚀 Dev Nimrod")
st.markdown(f"#### *Agentic {selected_lang.capitalize()} Auditor & Refactorer*")

# Input Area
code_input = st.text_area(f"Paste your {selected_lang} code here:", height=300, placeholder="// Your code goes here...")

if st.button("Run Multi-Agent Audit"):
    if not code_input:
        st.warning("Please provide code first!")
    else:
        with st.spinner(f"Agents are analyzing your {selected_lang} logic..."):
            # Refined prompt for Gemini 2.5/3 agents
            prompt = f"""
            Act as three expert agents (Security Specialist, Performance Engineer, Clean Code Architect).
            Analyze and refactor this {selected_lang} code.
            
            Return ONLY a valid JSON object. No other text.
            Required Keys: "refactored", "security_audit", "performance_audit", "architecture_audit", "complexity_score".
            
            CODE:
            {code_input}
            """
            
            try:
                response = model.generate_content(prompt)
                
                # Robust JSON extraction to avoid 404/parsing errors
                json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
                
                if json_match:
                    data = json.loads(json_match.group(0))
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.subheader(f"🛠️ Refactored {selected_lang.upper()}")
                        st.code(data['refactored'], language=selected_lang)
                        
                        st.divider()
                        st.subheader("🔍 Visual Comparison")
                        d_col1, d_col2 = st.columns(2)
                        with d_col1:
                            st.caption("Original")
                            st.code(code_input, language=selected_lang)
                        with d_col2:
                            st.caption("Refactored")
                            st.code(data['refactored'], language=selected_lang)

                    with col2:
                        st.subheader("🧠 Agent Findings")
                        st.success(f"**Complexity Score:** {data['complexity_score']}")
                        
                        with st.expander("🛡️ Security Specialist", expanded=True):
                            st.write(data['security_audit'])
                        
                        with st.expander("⚡ Performance Engineer", expanded=True):
                            st.write(data['performance_audit'])
                            
                        with st.expander("🏗️ Clean Code Architect", expanded=True):
                            st.write(data['architecture_audit'])
                else:
                    st.error("AI returned an unexpected format. Please try again.")

            except Exception as e:
                st.error(f"Execution Error: {str(e)}")
                st.info("Check if your API key has access to 'gemini-2.5-flash' in AI Studio.")
