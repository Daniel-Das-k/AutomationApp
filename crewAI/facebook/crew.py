from crewai import Crew, Process
from crewAI.facebook.agents import (
    facebook_content_compiler,
    facebook_content_formatter,
    facebook_drafting_agent,
    facebook_image_creator,
    facebook_refinement_agent,
    facebook_seo_agent
)
from crewAI.facebook.tasks import (
    drafting_task_facebook,
    editing_task_facebook,
    seo_task_facebook,
    chief_task_facebook,
    image_generate_task_facebook,
    format_content_task_facebook
)

class Facebook:
    def __init__(self,voice_assistant):
        self.voice_assistant = voice_assistant
        self.crew = Crew(
            agents=[facebook_drafting_agent,facebook_refinement_agent,facebook_seo_agent,facebook_content_compiler,facebook_image_creator,facebook_content_formatter],
            tasks=[drafting_task_facebook,editing_task_facebook,seo_task_facebook,chief_task_facebook,image_generate_task_facebook,format_content_task_facebook],
            process=Process.sequential,
            memory=True,
            cache=True,
            max_rpm=100,
            share_crew=True
        )

    def run(self):
        self.voice_assistant.speak("Topic: ")
        text = self.voice_assistant.get_audio()
        if len(text) > 1:
            result = self.crew.kickoff(inputs={'topic': text})
            print(result)

# if __name__ == "__main__":
#     generator = Facebook()

#     text = input("Enter the topic for the Facebook post: ")

#     result = generator.run(topic=text)
#     print(result)
