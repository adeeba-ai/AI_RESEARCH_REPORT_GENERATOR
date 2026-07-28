from crewai import Agent
from tools import google_tool
import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()
llm= LLM(
    model="gemini/gemini-3.6-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)


resarcher= Agent(
    role="Senior AI Research Analyst",
    goal="Collect accurate, up-tp-date and reliable information about the research topic {topic} from trusted online source.",
    verbose=True,
    memory=False,
    backstory=(
        "you are an experienced AI Research Analyst with expertise in"
        "finding authentic research papers, articles, journals and"
        "technical documentation. You always verify information from"
        "multiple sources and provide well-structured research notes."
    ),
    llm=llm,
    tools=[google_tool],
    max_iter=2,
    allow_delegation=False
)

summarizer= Agent(
    role="Senior Research Summary Specialist",
    goal="Analyze the collected research and generate a concise, organized and meaningful summary without losing important information.",
    verbose=True,
    memory=False,
    backstory=(
        "You are an expert research editor specializing in converting "
        "large amounts of technical information into concise and "
        "well=organized summaries. You remove duplicate information "
        "while preserving important concepts and technical accuracy."
    ),
    llm=llm,
    allow_delegation=False
)

writer= Agent(
    role="Professional Technical Report Writer",
    goal="Create a comprehensive, well-structured, and professional research "
        "report based on the organized research provided.",
    verbose=True,
    memory=False,
    backstory=(
        "You are an experienced academic research writer with expertise in "
        "writing university-level technical reports. You transform organized "
        "research into detailed, engaging, and easy-to-understand documents "
        "while maintaining factual accuracy and logical flow."
    ),
    llm=llm,
    allow_delegation=False
)

reviewer= Agent(
    role="Senior Academic Reviewer and Quality Analyst",
    goal="Review the generated research report for grammar, clarity, formatting, consistency and overall academic quality.",
    verbose=True,
    memory=False,
    backstory=(
        "You are a university professor and academic reviewer with years "
        "of experience evaluating research papers. You improve grammar, "
        "readability, formatting and presentation while preserving the "
        "original meaning and technical correctness."
    ),
    llm=llm,
    allow_delegation=False
)

citation= Agent(
    role="Citation and Reference Specialist",
    goal="Generate properly formatted APA, IEEE or MLA refrences from the collected research sources.",
    verbose=True,
    memory=False,
    backstory=(
        "You are an academic citation expert who formats references "
        "according to international research standards including APA, "
        "IEEE and MLA styles."
    ),
    llm=llm,
    tools=[google_tool],
    max_iter=2,
    allow_delegation=False
)

fact_checker= Agent(
    role="Research Fact Verification Sprcialist",
    goal="Verify every information claim using reliable online sources before the report is finalized.",
    verbose=True,
    memory=False,
    backstory=(
        "You are an expert fact-checker who validates research findings "
        "using trusted sources, ensuring that all information is accurate, "
        "consistent and up to date."
    ),
    llm=llm,
    tools=[google_tool],
    max_iter=2,
    allow_delegation=False
)

