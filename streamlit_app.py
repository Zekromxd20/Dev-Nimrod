import streamlit as st
import google.generativeai as genai
import json
import re

# 1. Setup
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash') 
    else:
        st.error("API Key missing! Please add it to Secrets.")
except Exception as e:
    st.error(f"Setup Error: {e}")

st.set_page_config(page_title="Dev Nimrod | AI Architect", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS FOR AESTHETICS ---
st.markdown("""
    <style>
    /* Main background and font */
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    
    /* Custom Card Style for Agent Findings */
    .agent-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #00ffcc;
        margin-bottom: 20px;
    }
    
    /* Header styling */
    h1, h2, h3 { font-family: 'Inter', sans-serif; color: #00ffcc !important; }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] { background-color: #161b22 !important; border-right: 1px solid #30363d; }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(45deg, #00ffcc, #007bff);
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        transition: 0.3s;
        width: 100%;
    }
    .stButton>button:hover { transform: scale(1.02); color: #fff; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80) # Generic AI icon
    st.title("Dev Nimrod v2")
    st.caption("Advanced Agentic Refactoring")
    st.divider()
    selected_lang = st.selectbox("🎯 Target Language", ["python", "cpp", "java", "javascript", "go", "rust"])
    st.info("The agents will now analyze your code for vulnerabilities and performance bottlenecks.")

# Main Header
st.title("🚀 Dev Nimrod: AI Architect")
st.markdown("### *Transforming Legacy Code into Optimized Logic*")

# Input
code_input = st.text_area("📥 Paste your source code here:", height=250, placeholder="Paste your messy code...")

if st.button("✨ START MULTI-AGENT AUDIT"):
    if not code_input:
        st.warning("Please enter code first!")
    else:
        with st.spinner("🤖 Consulting with Security, Performance, and Architecture Agents..."):
            prompt = f"""
            Act as 3 expert agents. Refactor this {selected_lang} code.
            Return ONLY a JSON object with: 
            "refactored", "security_audit", "performance_audit", "architecture_audit", "complexity_score".
            """
            
            try:
                response = model.generate_content(f"{prompt}\n\nCODE:\n{code_input}")
                json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
                
                if json_match:
                    data = json.loads(json_match.group(0))
                    
                    # Layout: Big Code Section, Sidebar-style Agent Findings
                    main_col, agent_col = st.columns([2, 1])
                    
                    with main_col:
                        st.subheader("🛠️ Refactored Result")
                        st.code(data['refactored'], language=selected_lang)
                        
                        with st.expander("🔍 View Comparison (Diff)"):
                            diff_1, diff_2 = st.columns(2)
                            diff_1.caption("Original")
                            diff_1.code(code_input, language=selected_lang)
                            diff_2.caption("Optimized")
                            diff_2.code(data['refactored'], language=selected_lang)

                    with agent_col:
                        st.subheader("🧠 Agent Intelligence")
                        st.metric("Complexity Score", data['complexity_score'])
                        
                        st.markdown(f"""
                        <div class="agent-card">
                            <h4>🛡️ Security Agent</h4>
                            <p>{data['security_audit']}</p>
                        </div>
                        <div class="agent-card" style="border-left-color: #ffcc00;">
                            <h4>⚡ Performance Agent</h4>
                            <p>{data['performance_audit']}</p>
                        </div>
                        <div class="agent-card" style="border-left-color: #007bff;">
                            <h4>🏗️ Architect Agent</h4>
                            <p>{data['architecture_audit']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error("Agent communication failed. Try again!")
            except Exception as e:
                st.error(f"Error: {e}")
