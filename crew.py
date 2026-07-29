from crewai import Crew, Process
from agents import resarcher, summarizer, writer, citation
from task import (
    research_task,
    summary_task,
    writer_task,
    citation_task,
)
from pdf_and_docx import generate_pdf, generate_docx
from podcast_generator import create_podcast
import os
 
crew = Crew(
        agents=[resarcher, summarizer, writer, citation],
        tasks=[
            research_task,
            summary_task,
            writer_task,
            citation_task,
        ],
    process=Process.sequential,
    memory=True,
    cache=True,
    max_rpm=12,
    share_crew=True,
)

def run_research(topic):
    result = crew.kickoff(inputs={"topic": topic})

    # Create output folder if it doesn't exist
    os.makedirs("output", exist_ok=True)

    # Make the filename safe for Windows
    safe_topic = "".join(c for c in topic if c not in r'<>:"/\|?*')

    pdf_path = f"output/{safe_topic}.pdf"
    docx_path = f"output/{safe_topic}.docx"
    podcast_path = f"output/{safe_topic}_podcast.mp3"
    markdown_path = f"output/{safe_topic}.md"

    # Save raw markdown
    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write(str(result))

    generate_pdf(str(result), pdf_path)
    generate_docx(str(result), docx_path)
    create_podcast(str(result), podcast_path)

    return str(result), pdf_path, docx_path, podcast_path, markdown_path

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        topic = sys.argv[1]
    else:
        topic = input("Enter the research topic: ")
        
    result, pdf_path, docx_path, podcast_path, markdown_path = run_research(topic)
    print(f"\nPDF saved as: {pdf_path}")
    print(f"DOCX saved as: {docx_path}")
    print(f"Podcast saved as: {podcast_path}")
    print(f"Markdown saved as: {markdown_path}")
    print("\nResearch completed successfully!")