from crewai import Crew, Process

from .agents import (
    discord_content_compiler,
    discord_formatting_agent,
    discord_drafting_agent,
    discord_refinement_agent,
    discord_seo_agent
)
from .tasks import (
    drafting_task_discord,
    editing_task_discord,
    seo_task_discord,
    chief_task_discord,
    format_content_task_discord
)

class Discord:
    def __init__(self):
        # self.voice_assistant = voice_assistant
        self.crew = Crew(
            agents=[
                discord_drafting_agent,
                discord_refinement_agent,
                discord_seo_agent,
                discord_content_compiler,
                discord_formatting_agent
            ],
            tasks=[
                drafting_task_discord,
                editing_task_discord,
                seo_task_discord,
                chief_task_discord,
                format_content_task_discord
            ],
            process=Process.sequential,
            memory=False,
            cache=True,
            max_rpm=100,
            share_crew=True
        )

    def run(self,content):
        # self.voice_assistant.speak("Please provide the topic: ")
        # topic = input("Please provide the topic: ")
        # topic = self.voice_assistant.get_audio()
        # self.voice_assistant.speak("Please provide the YouTube link: ")
        # youtube_link = self.voice_assistant.get_audio()
        youtube_link = input("Please provide the YouTube link: ")

        if len(content) > 1 and len(youtube_link) > 1:
            result = self.crew.kickoff(inputs={'topic': content, 'youtube_link': youtube_link})
            print(result)

# if __name__ == "__main__":
#     generator = Discord()
#     result = generator.run()