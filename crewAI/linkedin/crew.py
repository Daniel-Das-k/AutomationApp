from crewai import Crew, Process
from agents import drafting_agent, seo_optimization_agent, editing_refinement_agent, chief_agent
from tasks import drafting_task, seo_task, chief_task, editing_task

class LinkedIn:
    def __init__(self):
        self.agents = [drafting_agent,editing_refinement_agent,seo_optimization_agent,chief_agent]
        self.tasks = [drafting_task,editing_task,seo_task,chief_task]
        # # self.voice_assistant = voice_assistant
        
        self.crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            memory=True,
            cache=True,
            max_rpm=100,
            share_crew=True
        )

    def run(self):
        # self.voice_assistant.speak("Enter the Topic to be posted on : ")
        # text = self.voice_assistant.get_audio()
        text = input("Enter: ")
        if len(text) > 1:
            result = self.crew.kickoff(inputs={'topic': text})
            print(result)


if __name__ == "__main__":
    crew_runner = LinkedIn()
    crew_runner.run()
