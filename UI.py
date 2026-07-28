import streamlit as st
import os
import sys
import re
import contextlib
import io
from crew import run_research

# Page configuration
st.set_page_config(
    page_title="Research Pilot AI Report Generator",
    page_icon="logo.jpg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Styling
st.markdown("""
<style>
    /* Premium visual styles */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        margin: 0;
        font-family: 'Outfit', 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .main-header p {
        margin: 10px 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    .agent-card {
        background-color: rgba(30, 60, 114, 0.05);
        border-left: 5px solid #1e3c72;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 4px;
    }
    .dark .agent-card {
        background-color: rgba(255, 255, 255, 0.05);
        border-left: 5px solid #2a5298;
    }
    .agent-name {
        font-weight: 700;
        color: #1e3c72;
        margin-bottom: 0.2rem;
    }
    .dark .agent-name {
        color: #64b5f6;
    }
    .agent-goal {
        font-size: 0.9rem;
        font-style: italic;
    }
    .stButton>button {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.6rem 2rem !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(30, 60, 114, 0.3) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(30, 60, 114, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# Custom stdout redirector to capture CrewAI logs in real-time
class StreamToStreamlit:
    def __init__(self, placeholder):
        self.placeholder = placeholder
        self.text = ""
        self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    def write(self, text):
        clean_text = self.ansi_escape.sub('', text)
        self.text += clean_text
        # Display the log tail (last 10000 chars) in the Streamlit code block
        self.placeholder.code(self.text[-10000:])

    def flush(self):
        pass

# Sidebar contents
with st.sidebar:
    st.image("logo.jpg", use_container_width=True)
    st.markdown("### Research Pilot Info")
    st.markdown("This application deploys a sequential crew of 6 specialized AI agents to research, compose, and finalize a highly detailed report.")
    
    st.markdown("---")
    st.markdown("### 🤖 Swarm Members")
    
    agents = [
        {"name": "Senior AI Research Analyst", "goal": "Gather authentic research papers, websites & articles.", "icon": "🔍"},
        {"name": "Research Summary Specialist", "goal": "Consolidate information & eliminate redundancies.", "icon": "📄"},
        {"name": "Technical Report Writer", "goal": "Draft a comprehensive 2500-4000 word academic report.", "icon": "✍️"},
        {"name": "Academic Reviewer & Analyst", "goal": "Evaluate reports for grammar, style, and structure.", "icon": "🎓"},
        {"name": "Citation & Reference Specialist", "goal": "Verify sources and append standard IEEE citations.", "icon": "📚"},
        {"name": "Fact Verification Specialist", "goal": "Cross-check details and ensure scientific accuracy.", "icon": "✅"}
    ]
    
    for agent in agents:
        st.markdown(f"""
        <div class="agent-card">
            <div class="agent-name">{agent['icon']} {agent['name']}</div>
            <div class="agent-goal">Goal: {agent['goal']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("**Powered by CrewAI & Gemini 2.5 Flash**")

# Main Header UI
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("logo.jpg", use_container_width=True)
with col_title:
    st.markdown("""
    <div class="main-header" style="padding: 1.5rem; margin-bottom: 0; display: flex; flex-direction: column; justify-content: center; height: 100%;">
        <h1 style="margin: 0; font-size: 2.2rem;">Research Pilot AI Report Generator</h1>
        <p style="margin: 5px 0 0 0; font-size: 1rem;">Deploy an autonomous agentic crew to perform deep-dive web research, write a professional-grade academic report, fact-check it, and generate a downloadable podcast.</p>
    </div>
    """, unsafe_allow_html=True)
st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

# Initialize session state for topic
if "research_topic" not in st.session_state:
    st.session_state.research_topic = ""

# Main Topic input bound to session state
topic_input = st.text_input(
    "Enter the Research Topic:", 
    key="research_topic",
    placeholder="e.g., The Future of Nuclear Fusion Energy, Advancements in Quantum Computing in 2026",
    help="Provide a clear, descriptive topic for the agents to research."
)

# Topic selection callback function
def select_topic(topic_name):
    st.session_state.research_topic = topic_name

# Topic Quick-Select buttons
st.markdown("<small style='opacity:0.8;'>Quick Ideas:</small>", unsafe_allow_html=True)
cols = st.columns(3)
quick_topics = [
    "Quantum Computing Advancements in 2026",
    "Generative AI Impact on Cyber Security",
    "The Ethics of Brain-Computer Interfaces"
]

selected_topic = st.session_state.research_topic

for idx, qt in enumerate(quick_topics):
    cols[idx].button(qt, key=f"qt_{idx}", on_click=select_topic, args=(qt,))

# Display selected topic or wait for input
if selected_topic:
    st.info(f"Target Research: **{selected_topic}**")

# Start Research Button
run_button = st.button("🚀 Launch Research Swarm", use_container_width=True)

if run_button:
    if not selected_topic.strip():
        st.warning("Please enter a valid research topic first.")
    else:
        st.subheader("🤖 Live Agent Workspace")
        status_box = st.empty()
        log_placeholder = st.empty()
        
        try:
            status_box.info("Deploying AI research crew... Please check the agent execution logs below for real-time progress. This will take a few minutes.")
            
            # Execute the crew.py via subprocess
            import subprocess
            python_exe = os.path.join("myenv", "Scripts", "python.exe")
            if not os.path.exists(python_exe):
                python_exe = sys.executable
                
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            env["PYTHONUTF8"] = "1"
            env["OTEL_SDK_DISABLED"] = "true"
            
            # Sync API Keys to prevent conflicts where LiteLLM picks an invalid GOOGLE_API_KEY
            if "GEMINI_API_KEY" in env:
                env["GOOGLE_API_KEY"] = env["GEMINI_API_KEY"]
            elif "GOOGLE_API_KEY" in env:
                env["GEMINI_API_KEY"] = env["GOOGLE_API_KEY"]


            process = subprocess.Popen(
                [python_exe, "crew.py", selected_topic],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                encoding="utf-8",
                env=env
            )
            
            ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
            log_text = ""
            
            # Read stdout dynamically line-by-line
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                clean_line = ansi_escape.sub('', line)
                log_text += clean_line
                log_placeholder.code(log_text[-10000:])
                
            exit_code = process.wait()
            
            if exit_code == 0:
                status_box.success("🎉 Research Campaign completed successfully!")
                
                # Derive output paths
                safe_topic = "".join(c for c in selected_topic if c not in r'<>:"/\|?*')
                pdf_path = f"output/{safe_topic}.pdf"
                docx_path = f"output/{safe_topic}.docx"
                podcast_path = f"output/{safe_topic}_podcast.mp3"
                markdown_path = f"output/{safe_topic}.md"
                
                # Read markdown report
                if os.path.exists(markdown_path):
                    with open(markdown_path, "r", encoding="utf-8") as f:
                        report_text = f.read()
                else:
                    report_text = "Report generated, but the raw markdown file could not be read."
                
                st.markdown("---")
                st.subheader("📚 Generated Deliverables")
                
                # Create three columns for downloading files
                col_pdf, col_docx, col_audio = st.columns(3)
                
                # PDF Download
                if os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        pdf_bytes = f.read()
                    col_pdf.download_button(
                        label="📄 Download PDF Report",
                        data=pdf_bytes,
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf",
                        use_container_width=True
                    )
                else:
                    col_pdf.error("PDF generation failed.")
                    
                # DOCX Download
                if os.path.exists(docx_path):
                    with open(docx_path, "rb") as f:
                        docx_bytes = f.read()
                    col_docx.download_button(
                        label="📝 Download Word Document (DOCX)",
                        data=docx_bytes,
                        file_name=os.path.basename(docx_path),
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
                else:
                    col_docx.error("DOCX generation failed.")
                    
                # Podcast Download & Audio Player
                if os.path.exists(podcast_path):
                    with open(podcast_path, "rb") as f:
                        podcast_bytes = f.read()
                    col_audio.download_button(
                        label="🎵 Download Audio Podcast (MP3)",
                        data=podcast_bytes,
                        file_name=os.path.basename(podcast_path),
                        mime="audio/mp3",
                        use_container_width=True
                    )
                    
                    # Audio Player Widget
                    st.markdown("### 🎙️ Listen to the Podcast Summary")
                    st.audio(podcast_path, format="audio/mp3")
                else:
                    col_audio.error("Audio podcast generation failed.")
                    
                # Preview report content
                st.markdown("---")
                st.subheader("📝 Report Preview")
                with st.expander("Show Final Report", expanded=True):
                    st.markdown(report_text)
            else:
                status_box.error(f"Research campaign failed with exit code: {exit_code}. Check the logs above for details.")
                
        except Exception as e:
            status_box.error(f"An error occurred during execution: {str(e)}")
            st.exception(e)

# Footer
st.markdown("""
<hr>
<div style="text-align: center; font-size: 0.85rem; opacity: 0.8; margin-top: 2rem; padding-bottom: 2rem;">
    Research Pilot AI Report Generator Web UI • Built with Streamlit, CrewAI & Gemini 2.5 Flash
</div>
""", unsafe_allow_html=True)
