# 🚀 Dev Nimrod | Multi-Agent AI Code Auditor

**Dev Nimrod** is a state-of-the-art Agentic AI system designed to audit, refactor, and optimize codebases. Built for the 2026 Hackathon, it moves beyond simple chat interfaces by employing a "Multi-Agent" strategy to ensure code is secure, performant, and architecturally sound.

https://dev-nimrod.streamlit.app/

## 🌟 Key Features
- **Multi-Agent Orchestration:** Simultaneously triggers three specialized AI agents—Security, Performance, and Architecture—to analyze code from distinct technical perspectives.
- **Agentic Refactoring:** Automatically rewrites code to improve time complexity (e.g., $O(n^2) \rightarrow O(n)$) and memory safety.
- **Multi-Language Support:** Context-aware auditing for Python, C++, Java, JavaScript, Go, and Rust.
- **Visual Intelligence Dashboard:** A sleek, dark-themed UI featuring "Glassmorphism" cards for agent findings and a side-by-side code comparison.
- **Complexity Tracking:** Real-time metrics showing algorithmic improvements and performance gains.

## 🧠 Technical Architecture
Dev Nimrod utilizes a sophisticated **System Prompting** technique to force the Gemini 2.5/3 Flash model into a structured JSON output. This allows the application to parse raw AI reasoning into a data-driven dashboard.

- **Frontend:** Streamlit (Custom CSS injected for Dark Mode)
- **AI Engine:** Google Gemini 2.5 Flash
- **Logic:** Regex-based JSON extraction for robust response parsing

## 🗺️ Technical Roadmap: The Future of Dev Nimrod

As a first-year CSE student, our vision for Dev Nimrod extends beyond simple file refactoring. Here is the planned evolution:

### 🟢 Phase 1: Contextual Awareness (Short Term)
- **Repository-Level Analysis:** Moving from single-file analysis to full-repo context using RAG (Retrieval-Augmented Generation).
- **GitHub Action Integration:** Automatically audit every Pull Request and leave agent comments on lines with vulnerabilities.

### 🟡 Phase 2: IDE Deep Integration (Mid Term)
- **VS Code Extension:** Bring Dev Nimrod agents directly into the editor via a custom extension.
- **LSP Support:** Implementing Language Server Protocol to provide real-time squiggly lines for "Agent Findings."

### 🔴 Phase 3: Autonomous Self-Correction (Long Term)
- **Unit Test Generation:** Agents will not only refactor code but also generate a `test.py` file to prove the new code works and passes all edge cases.
- **Self-Healing CI/CD:** If a build fails, Dev Nimrod agents will autonomously analyze the logs and propose a fix.

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/Zekromxd20/Dev-Nimrod.git](https://github.com/Zekromxd20/Dev-Nimrod.git)
cd Dev-Nimrod```


### 2. Install Dependencies
```bash

pip install -r requirements.txt```


### 3. Configure Secrets
Create a .streamlit/secrets.toml file (not tracked by Git) and add your API key:

GOOGLE_API_KEY = "your_actual_api_key_here"


### 4. Run Locally

streamlit run streamlit_app.py


🛡️ Security
Dev Nimrod follows "Privacy-by-Design." All API keys are managed via Streamlit Secrets and are never hardcoded or pushed to public version control.


👩‍💻  Developer 

**• Shubhi Bunkar -** First-Year B.Tech CSE Student

**• Kartick Thakur -** First-Year B.Tech CSE Student



