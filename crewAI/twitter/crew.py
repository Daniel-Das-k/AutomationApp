import os
import json
from dotenv import load_dotenv
load_dotenv()
import tweepy
import re
from crewai import  Crew
from crewai.process import Process
from .tasks import topic_analysis,content_research,create_twitter_posts
from .agents import trending_topic_researcher_agent,content_researcher_agent,creative_content_creator_agent

class Twitter:
	def __init__(self):
		# self.voice_assistant = voice_assistant
		self.crew = Crew(
			agents=[trending_topic_researcher_agent,content_researcher_agent,creative_content_creator_agent],
			tasks=[topic_analysis,content_research,create_twitter_posts],
			process=Process.sequential,
			memory=True,
            cache=True,
            max_rpm=100,
            share_crew=True
		)

	def run(self):
		# self.voice_assistant.speak("Say the topic to tweet about: ")
		# text = self.voice_assistant.get_audio()
		text = input("Enter the topic to tweet about: : ")
		result = self.crew.kickoff(inputs={'topic': text})
		print(result)
		return result
   

