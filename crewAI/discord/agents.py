import os
from crewai import Agent
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.search_tools import search_tool
import torch

if torch.backends.mps.is_available():
    mps_device = torch.device("mps")
    print("Running on MPS")
else:
    print("MPS device not found.")

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

discord_drafting_agent = Agent(
    role='Discord Message Specialist',
    goal="Generate engaging and relevant initial drafts for Discord posts based on specified topics and YouTube video insights.",
    verbose=True,
    memory=True,
    backstory="Specializes in creating engaging and relevant Discord messages tailored to the community's interests and communication style.",
    tools=[search_tool], 
    llm=llm,
    allow_delegation=True,
)

discord_refinement_agent = Agent(
    role='Discord Message Refinement Specialist',
    goal="Refine and enhance drafted Discord messages to ensure clarity, engagement, and coherence.",
    verbose=True,
    memory=True,
    backstory="Focuses on improving the clarity and impact of Discord messages, ensuring they are polished and resonate with the community.",
    tools=[search_tool], 
    llm=llm,
    allow_delegation=True,
)

discord_seo_agent = Agent(
    role='Discord SEO and Content Optimization Specialist',
    goal="Optimize Discord messages for discoverability and engagement by identifying and integrating relevant keywords and tags.",
    verbose=True,
    memory=True,
    backstory="Skilled in SEO strategies, this agent enhances message visibility and engagement within the Discord platform.",
    tools=[search_tool],  
    llm=llm,
    allow_delegation=True,
)

discord_content_compiler = Agent(
    role="Chief Discord Content Compiler",
    goal="Aggregate outputs from Drafting, Refinement, SEO, and Media Integration Agents into cohesive and optimized Discord posts.",
    verbose=True,
    memory=True,
    backstory="Specializes in synthesizing various content elements into a unified and engaging post that aligns with Discord's best practices.",
    tools=[search_tool],  
    llm=llm,
    allow_delegation=False,
)

discord_formatting_agent = Agent(
    role='Content Formatter for Discord',
    goal="Format content for Discord posts, ensuring they are visually appealing, well-structured, and easy to read.",
    verbose=True,
    memory=True,
    backstory="Focuses on presenting content effectively on Discord, enhancing readability and engagement.",
    tools=[],  
    llm=llm,
    allow_delegation=False,
)
