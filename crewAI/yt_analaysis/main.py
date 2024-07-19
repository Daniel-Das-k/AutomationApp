from crewai import Crew, Process
import os
from agents import YoutubeAutomationAgents
from tasks import YoutubeAutomationTasks
from tools.youtube_video_details_tool import YoutubeVideoDetailsTool
from tools.youtube_video_search_tool import YoutubeVideoSearchTool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                             verbose=True,
                             temperature=0.5,
                             google_api_key=os.getenv("GOOGLE_API_KEY"))

agents = YoutubeAutomationAgents()
tasks = YoutubeAutomationTasks()

youtube_video_search_tool = YoutubeVideoSearchTool()
youtube_video_details_tool = YoutubeVideoDetailsTool()

youtube_manager = agents.youtube_manager()
research_manager = agents.research_manager(
    youtube_video_search_tool, youtube_video_details_tool)
title_creator = agents.title_creator()
description_creator = agents.description_creator()
email_creator = agents.email_creator()

video_topic = "Full next JS course"
video_details = """
This video will teach you the full course on next js from beginning to the last we will cover all the concepts involved in it 
This is a beginner friendly course. we will dive into the advance concepts and build your programming languag from this course
"""

manage_youtube_video_creation = tasks.manage_youtube_video_creation(
    agent=youtube_manager,
    video_topic=video_topic,
    video_details=video_details
)
manage_youtube_video_research = tasks.manage_youtube_video_research(
    agent=research_manager,
    video_topic=video_topic,
    video_details=video_details,
)
create_youtube_video_title = tasks.create_youtube_video_title(
    agent=title_creator,
    video_topic=video_topic,
    video_details=video_details
)
create_youtube_video_description = tasks.create_youtube_video_description(
    agent=description_creator,
    video_topic=video_topic,
    video_details=video_details
)
create_email_announcement_for_new_video = tasks.create_email_announcement_for_new_video(
    agent=email_creator,
    video_topic=video_topic,
    video_details=video_details
)


# Create a new Crew instance
crew = Crew(
    agents=[youtube_manager,
            research_manager,
            email_creator,
            ],
    tasks=[manage_youtube_video_creation,
           manage_youtube_video_research,
           create_email_announcement_for_new_video],
    process=Process.hierarchical,
    manager_llm=llm
)

# Kick of the crew
results = crew.kickoff()

print("Crew usage", crew.usage_metrics)

print("Crew work results:")
print(results)
