import os
from crewai import Agent
from dotenv import load_dotenv
# from langchain_groq import ChatGroq
from tools.websearch import search_tool
from langchain_google_genai import ChatGoogleGenerativeAI
import torch
from crewai import Task
from crewai import Crew, Process

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                             verbose=True,
                             temperature=0.5,
                             google_api_key=os.getenv("GOOGLE_API_KEY"))


instagram_image_creator = Agent(
    role="Professional Image Creator for Instagram Posts",
    goal=(
        "To produce visually appealing and contextually relevant images that enhance engagement and resonate with Instagram's audience. "
        "Each image should align with the post's theme, reflect the brand's identity, and captivate Instagram users."
    ),
    backstory=(
        "An AI with a keen eye for design, specializing in creating visuals that amplify the message of Instagram posts. "
        "Leveraging advanced image generation technology and a deep understanding of Instagram's visual trends, it crafts images that capture attention and drive engagement, tailored to resonate with Instagram's diverse audience."
    ),
    verbose=True,
    llm=llm,
)

image_generate_task_instagram = Task(
    description=(
        "Create visually compelling image that capture and enhance the essence of an Instagram post about {topic}. "
        "The image should be relevant to the content of the post, reflecting the tone and aesthetic of Instagram. "
        "Focus on creating an image that add visual appeal and effectively convey the message to engage the Instagram audience."
        "Imagine what the photo you wanna take describe it in a paragraph."
			"Here are some examples for you to follow:"
			"- high tech airplaine in a beautiful blue sky in a beautiful sunset super cripsy beautiful 4k, professional wide shot"
			"- the last supper, with Jesus and his disciples, breaking bread, close shot, soft lighting, 4k, crisp"
			"- an bearded old man in the snows, using very warm clothing, with mountains full of snow behind him, soft lighting, 4k, crisp, close up to the camera"

			"Think creatively and focus on how the image can capture the audience's attention."
    ),
    agent=instagram_image_creator,  
    expected_output=(
        "The photograph that visually represent and complement the Instagram post on {topic}. "
        "The image should be professional, engaging, and aligned with Instagram's aesthetic and tone. "
        "Include a paragraph describing the photograph, detailing how it captures the essence of the post and engages the Instagram audience."
    ),
)

class InstagramImage:
    def __init__(self):
        # self.voice_assistant = voice_assistant
        self.crew = Crew(
            agents=[instagram_image_creator],
            tasks=[image_generate_task_instagram],
            process=Process.sequential,
            memory=False,
            cache=True,
            max_rpm=100,
            share_crew=True
        )

    def run(self,topic):
        # self.voice_assistant.speak("Say the Topic: ")
        # text = self.voice_assistant.get_audio()
        if len(topic) > 1:
            result = self.crew.kickoff(inputs={'topic': topic})
            print(result)

if __name__ == "__main__":
    generator = InstagramImage()

    text = input("Enter the topic for the Instagram post: ")

    result = generator.run(topic=text)
    print(result)