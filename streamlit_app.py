import streamlit as st
import google.generativeai as genai
import json

# 1. Setup - Using Streamlit Secrets
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Using Gemini 1.5 Flash for the fastest hackathon response times
    model = genai.GenerativeModel('gemini-1.5-flash') 
except Exception as e:
    st.error("API Key not found. Go to Settings > Secrets and add GOOGLE_API_KEY")

st.set_page_config(page_title="Dev Nimrod | AI Code Auditor", layout="wide")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stCodeBlock { border: 1px solid #30363d; }
    </style>
    """, unsafe_base64=True)

st.title("🚀 Dev Nimrod")
st.markdown("#### *Agentic Multi-Agent Code Auditing & Refactoring*")

# Input area
code_input = st.text_area("Paste your code here (Python, C++, JS, etc.):", height=250)

if st.button("Run Multi-Agent Audit"):
    if not code_input:
        st.warning("Please provide code first!")
    else:
        with st.spinner("Agents are analyzing (Security, Performance, Readability)..."):
            # Multi-Agent System Prompt
            prompt = f"""
            Act as a team of three expert agents: 
            1. Security Specialist 
            2. Performance Engineer 
            3. Clean Code Architect.
            
            Audit and refactor the following code. 
            Return ONLY a JSON object with:
            {{
                "refactored": "the full improved code",
                "security_audit": "one specific security finding",
                "performance_audit": "one specific performance finding",
                "architecture_audit": "one specific clean code finding",
                "complexity_score": "e.g., O(n^2) -> O(n)"
            }}
            CODE: {code_input}
            """
            
            response = model.generate_content(prompt)
            
            try:
                # Cleaning the AI output
                res_text = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(res_text)
                
                # Layout: Left side for Code, Right side for Agent findings
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write("### 🛠️ Refactored Output")
                    st.code(data['refactored'], language='python')
                    
                    # Manual Diff View using standard columns
                    st.divider()
                    diff_col1, diff_col2 = st.columns(2)
                    with diff_col1:
                        st.caption("Original")
                        st.code(code_input)
                    with diff_col2:
                        st.caption("Refactored")
                        st.code(data['refactored'])

                with col2:
                    st.write("### 🧠 Agent Findings")
                    st.success(f"**Complexity:** {data['complexity_score']}")
                    
                    with st.expander("🛡️ Security Agent", expanded=True):
                        st.write(data['security_audit'])
                    
                    with st.expander("⚡ Performance Agent", expanded=True):
                        st.write(data['performance_audit'])
                        
                    with st.expander("🏗️ Architecture Agent", expanded=True):
                        st.write(data['architecture_audit'])
                
            except Exception as e:
                st.error(f"Error parsing agent logic. Click Refactor again! Error: {e}")
