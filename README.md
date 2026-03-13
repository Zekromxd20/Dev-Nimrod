# 🏹 Dev Nimrod: Multi-Agent Bug Hunter

**Dev Nimrod** is an autonomous, agentic AI system designed to audit, detect, and refactor code across multiple programming languages. Developed for the **IIT Bombay Hack & Break 2026**, it moves beyond simple chatbots by using a dual-agent reasoning chain to ensure code safety and industrial-grade quality.

## 🚀 Live Demo
[Explore Dev Nimrod Live](https://dev-nimrod.streamlit.app) *(Replace with your actual URL)*

---

## 🕵️ The Agentic Architecture
Dev Nimrod operates using two specialized AI agents powered by **Gemini 3 Flash-Preview**:

1. **The Auditor Agent:** Performs deep semantic analysis to find "Nimrod" mistakes—logical fallacies, memory leaks, buffer overflows, and security vulnerabilities that standard compilers might miss.
2. **The Master Smith Agent:** Takes the Auditor’s report and the original source code to "forge" a refactored version that follows modern best practices (e.g., RAII in C++, PEP8 in Python).

---

## ✨ Features
* **Multi-Language Support:** Calibrated for C, C++, Python, Java, JavaScript, and SQL.
* **Real-time Agent Tracking:** Animated status bars show the collaboration between the Auditor and the Smith.
* **Logic-First Auditing:** Goes beyond syntax to find runtime risks like Division by Zero and Pointer Mismanagement.
* **Cloud-Native & Serverless:** Built with Streamlit and deployed for 100% availability.

---

## 🛠️ Tech Stack
* **Engine:** Google Gemini 3 Flash-Preview (Agentic Reasoning)
* **Frontend:** Streamlit (Reactive UI)
* **Language:** Python 3.12+
* **Deployment:** Streamlit Community Cloud & GitHub

---

## 🏃 How to Run Locally
1. Clone the repo:
   ```bash
   git clone [https://github.com/your-username/Dev-Nimrod.git](https://github.com/your-username/Dev-Nimrod.git)
