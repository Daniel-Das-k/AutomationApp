from crewai import Crew ,Process
from .agents import instagram_content_compiler,instagram_content_formatter,instagram_drafting_agent,instagram_image_creator,instagram_refinement_agent,instagram_seo_agent
from .tasks import drafting_task_instagram,editing_task_instagram,seo_task_instagram,chief_task_instagram,image_generate_task_instagram,format_content_task_instagram

class Instagram:
    def __init__(self,voice_assistant):
        self.voice_assistant = voice_assistant
        self.crew = Crew(
            agents=[instagram_drafting_agent,instagram_refinement_agent,instagram_seo_agent,instagram_content_compiler,instagram_image_creator,instagram_content_formatter],
            tasks=[drafting_task_instagram,editing_task_instagram,seo_task_instagram,chief_task_instagram,image_generate_task_instagram,format_content_task_instagram],
            process=Process.sequential,
            memory=True,
            cache=True,
            max_rpm=100,
            share_crew=True
        )

    def run(self):
        self.voice_assistant.speak("Say the Topic: ")
        text = self.voice_assistant.get_audio()
        if len(text) > 1:
            result = self.crew.kickoff(inputs={'topic': text})
            print(result)

