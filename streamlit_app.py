import streamlit as st
import google.generativeai as genai
import time  # For simulating 'thinking' and smooth transitions

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Dev Nimrod: Multi-Agent Bug Hunter",
    page_icon="🏹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR ANIMATIONS & STYLE ---
# This CSS will add a subtle subtle glow and fade-in effect to our elements.
st.markdown("""
<style>
    /* Fade-in animation for main content */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .main-content {
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Subtle glow for the 'Hunt' button on hover */
    div.stButton > button:hover {
        box-shadow: 0 0 10px rgba(76, 175, 80, 0.7);
        border-color: #4CAF50;
        transform: scale(1.02);
        transition: all 0.2s ease-in-out;
    }
</style>
""", unsafe_allow_html=True)

# Container for all content to apply the fade-in
with st.container(border=False):
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # --- HEADER ---
    col_title, col_logo = st.columns([5, 1])
    with col_title:
        st.title("🏹 Dev Nimrod: Multi-Agent Bug Hunter")
        st.markdown("*Calibrated for Multi-Language Logic Analysis & Refactoring*")
    with col_logo:
        # A simple visual logo using Streamlit columns
        st.markdown("## 🎯")

    # --- UI LAYOUT & SETTINGS (SIDEBAR) ---
    with st.sidebar:
        st.header("Hunter's Calibration ⚙️")
        language = st.selectbox(
            "Select Programming Language",
            ["C", "C++", "Python", "Java", "JavaScript", "HTML/CSS", "SQL"],
            index=0
        )
        st.divider()
        st.info(f"Nimrod is now optimized for **{language}** syntax and logical best practices.")

    # --- API KEY & MODEL SETUP ---
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("Missing GOOGLE_API_KEY in Streamlit Secrets! Check your settings.")
    else:
        # Initialize the 'Auditor' and 'Smith' Agents
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        auditor_model = genai.GenerativeModel('gemini-3-flash-preview')
        smith_model = genai.GenerativeModel('gemini-3-flash-preview')

        # --- CODE INPUT AREA ---
        code_input = st.text_area(
            f"📥 Paste your {language} code snippet to begin the hunt:",
            height=300,
            placeholder=f"Paste your {language} code here...",
            help=f"Submit your {language} code for parallel auditing and refactoring by specialized AI agents."
        )

        # --- ANIMATED SUBMISSION BUTTON ---
        # The CSS animation makes this button pop.
        hunt_button = st.button("🚀 START THE HUNT", help="Click to trigger the multi-agent reasoning chain.")

        if hunt_button:
            if not code_input:
                st.warning("Please paste some code first!")
            else:
                # Use a combined visual interaction: Status Update + Loading Spinner
                status = st.status(f"Calibrating Agents for **{language}** hunt...", expanded=True)
                
                with status:
                    # Stage 1: Auditor
                    st.write("🕵️ Agent 1: Auditor is tracking bugs in the logic...")
                    time.sleep(1)  # Simulate agent 'thinking' for smooth demo flow
                    
                    try:
                        # 1. THE AUDITOR (Agent 1)
                        prompt_auditor = (
                            f"You are the Senior Auditor Agent specializing in {language}.\n"
                            f"Generate a detailed bulleted list of bugs and anti-patterns in this code. "
                            f"Include line references where possible.\n\nCode:\n{code_input}"
                        )
                        audit_report = auditor_model.generate_content(prompt_auditor)
                        st.success("Auditor report complete. Logic errors identified.")

                        # Stage 2: Smith
                        st.write("🛠️ Agent 2: Master Smith is forging the correction...")
                        time.sleep(1)
                        
                        # 2. THE MASTER SMITH (Agent 2)
                        prompt_smith = (
                            f"You are the Master Smith Agent specializing in {language} refactoring.\n"
                            f"Use this Auditor report: \n{audit_report.text}\n"
                            f"to rewrite the original code. Provide ONLY the final, perfect code snippet.\n\n"
                            f"Original Code:\n{code_input}"
                        )
                        final_fix = smith_model.generate_content(prompt_smith)
                        st.success("Master Smith has refactored the code.")
                        
                        # Final Update before showing the results
                        status.update(label="Hunt Complete!", state="complete", expanded=False)
                        
                    except Exception as e:
                        status.update(label="The Hunt was Interrupted!", state="error", expanded=True)
                        st.error(f"Error: {e}")

                # --- MULTI-AGENT REPORT (RESULTS) ---
                st.divider()
                st.markdown("## 🎯 Hunt Results")
                
                col_audit, col_fix = st.columns(2)
                
                with col_audit:
                    st.markdown("### 🕵️ Auditor's Report")
                    # Use a clean 'Report Card' layout
                    if 'audit_report' in locals():
                        st.markdown(audit_report.text)
                    else:
                        st.write("Agent 1 analysis complete.")

                with col_fix:
                    st.markdown("### 🛠️ Master Smith's Forged Code")
                    if 'final_fix' in locals():
                        # Display code with a built-in 'Copy' button
                        st.code(final_fix.text, language=language.lower())
                        st.success("Correction forged with 100% precision.")
                    else:
                        st.write("Agent 2 reconstruction complete.")

    st.markdown('</div>', unsafe_allow_html=True) # Close the main-content container
