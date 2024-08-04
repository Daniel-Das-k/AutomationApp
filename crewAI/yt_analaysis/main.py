# from crewai import Crew, Process
# import os
# from agents import YoutubeAutomationAgents
# from tasks import YoutubeAutomationTasks
# from tools.youtube_video_details_tool import YoutubeVideoDetailsTool
# from tools.youtube_video_search_tool import YoutubeVideoSearchTool
# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv

# load_dotenv()

# llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
#                              verbose=True,
#                              temperature=0.5,
#                              google_api_key=os.getenv("GOOGLE_API_KEY"))

# agents = YoutubeAutomationAgents()
# tasks = YoutubeAutomationTasks()

# youtube_video_search_tool = YoutubeVideoSearchTool()
# youtube_video_details_tool = YoutubeVideoDetailsTool()

# youtube_manager = agents.youtube_manager()
# research_manager = agents.research_manager(
#     youtube_video_search_tool, youtube_video_details_tool)
# title_creator = agents.title_creator()
# description_creator = agents.description_creator()
# email_creator = agents.email_creator()

# video_topic = "Full next JS course"
# video_details = """
# This video will teach you the full course on next js from beginning to the last we will cover all the concepts involved in it 
# This is a beginner friendly course. we will dive into the advance concepts and build your programming languag from this course
# """

# manage_youtube_video_creation = tasks.manage_youtube_video_creation(
#     agent=youtube_manager,
#     video_topic=video_topic,
#     video_details=video_details
# )
# manage_youtube_video_research = tasks.manage_youtube_video_research(
#     agent=research_manager,
#     video_topic=video_topic,
#     video_details=video_details,
# )
# create_youtube_video_title = tasks.create_youtube_video_title(
#     agent=title_creator,
#     video_topic=video_topic,
#     video_details=video_details
# )
# create_youtube_video_description = tasks.create_youtube_video_description(
#     agent=description_creator,
#     video_topic=video_topic,
#     video_details=video_details
# )
# create_email_announcement_for_new_video = tasks.create_email_announcement_for_new_video(
#     agent=email_creator,
#     video_topic=video_topic,
#     video_details=video_details
# )


# # Create a new Crew instance
# crew = Crew(
#     agents=[youtube_manager,
#             research_manager,
#             email_creator,
#             ],
#     tasks=[manage_youtube_video_creation,
#            manage_youtube_video_research,
#            create_email_announcement_for_new_video],
#     process=Process.hierarchical,
#     manager_llm=llm,
#     memory=False
# )

# # Kick of the crew
# results = crew.kickoff()

# print("Crew usage", crew.usage_metrics)

# print("Crew work results:")
# print(results)
 

from crewai import Crew, Process
import os
from .agents import YoutubeAutomationAgents
from .tasks import YoutubeAutomationTasks
from .tools.youtube_video_details_tool import YoutubeVideoDetailsTool
from .tools.youtube_video_search_tool import YoutubeVideoSearchTool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

class YoutubeAutomationProcess:
    def __init__(self):
        load_dotenv()
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                                          verbose=True,
                                          temperature=0.5,
                                          google_api_key=os.getenv("GOOGLE_API_KEY"))
        self.agents = YoutubeAutomationAgents()
        self.tasks = YoutubeAutomationTasks()
        self.youtube_video_search_tool = YoutubeVideoSearchTool()
        self.youtube_video_details_tool = YoutubeVideoDetailsTool()

    def setup_agents(self):
        self.youtube_manager = self.agents.youtube_manager()
        self.research_manager = self.agents.research_manager(
            self.youtube_video_search_tool, self.youtube_video_details_tool)
        self.title_creator = self.agents.title_creator()
        self.description_creator = self.agents.description_creator()
        self.email_creator = self.agents.email_creator()

    def generate_title(self, video_topic, video_details):
        task = self.tasks.create_youtube_video_title(
            agent=self.title_creator,
            video_topic=video_topic,
            video_details=video_details
        )
        title_crew = Crew(
            agents=[self.title_creator],
            tasks=[task],
            process=Process.hierarchical,
            manager_llm=self.llm,
            memory=False
        )
        results = title_crew.kickoff()
        return results

    def generate_description(self, video_topic, video_details):
        task = self.tasks.create_youtube_video_description(
            agent=self.description_creator,
            video_topic=video_topic,
            video_details=video_details
        )
        description_crew = Crew(
            agents=[self.description_creator],
            tasks=[task],
            process=Process.hierarchical,
            manager_llm=self.llm,
            memory=False
        )
        results = description_crew.kickoff()
        return results

    def generate_email(self, video_topic, video_details):
        task = self.tasks.create_email_announcement_for_new_video(
            agent=self.email_creator,
            video_topic=video_topic,
            video_details=video_details
        )
        email_crew = Crew(
            agents=[self.email_creator],
            tasks=[task],
            process=Process.hierarchical,
            manager_llm=self.llm,
            memory=False
        )
        results = email_crew.kickoff()
        return results

    def generate_title_and_description(self, video_topic, video_details):
        title = self.generate_title(video_topic, video_details)
        description = self.generate_description(video_topic, video_details)
        return title, description

    def setup_tasks(self, video_topic, video_details):
        self.manage_youtube_video_creation = self.tasks.manage_youtube_video_creation(
            agent=self.youtube_manager,
            video_topic=video_topic,
            video_details=video_details
        )
        self.manage_youtube_video_research = self.tasks.manage_youtube_video_research(
            agent=self.research_manager,
            video_topic=video_topic,
            video_details=video_details,
        )
        self.create_email_announcement_for_new_video = self.tasks.create_email_announcement_for_new_video(
            agent=self.email_creator,
            video_topic=video_topic,
            video_details=video_details
        )

    def kickoff_crew(self):
        self.crew = Crew(
            agents=[self.youtube_manager, self.research_manager, self.email_creator],
            tasks=[self.manage_youtube_video_creation, self.manage_youtube_video_research, self.create_email_announcement_for_new_video],
            process=Process.hierarchical,
            manager_llm=self.llm,
            memory=False
        )
        results = self.crew.kickoff()
        return results, self.crew.usage_metrics


if __name__ == '__main__':
    video_topic = "Full Next.js course"
    video_details = """
    This video will teach you the full course on Next.js from beginning to end. We will cover all the concepts involved in it. 
    This is a beginner-friendly course. We will dive into the advanced concepts and build your programming skills from this course.
    """
    
    youtube_automation = YoutubeAutomationProcess()
    youtube_automation.setup_agents()
    
    # Generate title and description
    title, description = youtube_automation.generate_title_and_description(video_topic, video_details)
    
    # Generate email
    email = youtube_automation.generate_email(video_topic, video_details)
    
    # Print title, description, and email
    print("Generated Title:", title)
    print("Generated Description:", description)
    print("Generated Email:", email)
