from crewai import Task
from  tools import google_tool
from agents import resarcher,summarizer,writer,citation

research_task= Task(
    description=(
        "Research the given topic '{topic}'. "

        "Collect accurate, up-to-date and reliable information from trusted "
        "online sources including research papers, official websites and "
        "technical articles. "

        "Identify the major concepts, applications, advantages, challenges, "
        "future scope and references related to the topic."
    ),

    expected_output=(
        "A comprehensive research document containing verified information, "
        "important facts, key points and source URLs related to the given topic."
    ),

    tools=[google_tool],
    agent=resarcher
)

summary_task= Task(
    description=(
        "Analyze the research collected by the Research Agent. "

        "Remove duplicate information, unnecessary details and irrelevant "
        "content while preserving all important concepts. "

        "Organize the information into structured sections."
    ),

    expected_output=(
        "A concise and well-structured summary organized into sections such as "
        "Introduction, Applications, Advantages, Challenges and Future Scope."
    ),

    agent=summarizer,
    context=[research_task]
)

writer_task= Task(
    description=(
        "Using the organized research provided, write a detailed research report. "
        "The report should be approximately 2500-4000 words and include:\n\n"
        "1. Title\n"
        "2. Abstract\n"
        "3. Table of Contents\n"
        "4. Introduction\n"
        "5. Background\n"
        "6. Detailed Explanation of the Topic\n"
        "7. Working Principles (if applicable)\n"
        "8. Applications\n"
        "9. Advantages\n"
        "10. Challenges and Limitations\n"
        "11. Recent Developments\n"
        "12. Future Scope\n"
        "13. Conclusion\n\n"
        "Use clear headings and professional academic language. Expand each "
        "section with detailed explanations instead of brief summaries."
    ),

    expected_output=(
        "A professional research report with well-structured sections, "
        "detailed explanations, and approximately 2500-4000 words."
    ),

    agent=writer,
    context=[summary_task]
)



citation_task= Task(
    description=(
        "Take the complete reviewed research report from the previous task. "
        "Do NOT remove or rewrite the report. "
        "Generate properly formatted citations for every source used during research. "
        "Append the references at the end of the report in IEEE format."
        "Take the complete reviewed research report from the previous task. "
        "Analyze all factual statements and identify the sources used. "
        "Use Google Search to find the original authors, publication year, "
        "journal/conference or website, DOI (if available), and other "
        "bibliographic information. "
        "Generate accurate IEEE citations and append them to the end of the report. "
        "Do NOT remove, shorten, rewrite, or replace any part of the report."
    ),

    expected_output=(
        "The complete research report with an IEEE References section appended at the end."
    ),
    
    tools=[google_tool],
    agent=citation,
    context=[writer_task]
)



