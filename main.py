

import time
from datetime import datetime
from dateutil import parser, relativedelta
import re
from crewAI.discord.crew import Discord
# from imgvidgen import TextToVideoGenerator,ImageGenerator
# from crewAI.email.src.graph import WorkFlow
from crewAI.facebook.crew import Facebook
from crewAI.youtube.yt_upload import YouTubeUploader
from crewAI.instagram.crew import Instagram
from crewAI.linkedin.crew import LinkedIn
from crewAI.twitter.crew import Twitter
from crewAI.summarization.summarize import Summarizer
from crewAI.yt_summarizer.ytTransSummarizer import YouTubeTranscriptSummarizer
from voice import VoiceAssistant
from crewAI.yt_analaysis.main import YoutubeAutomationProcess


title_description = YoutubeAutomationProcess()

# voice_assistant = VoiceAssistant()
# video_gen = TextToVideoGenerator()
# img_gen = ImageGenerator()
facebook = Facebook()
instagram = Instagram()
linkedin = LinkedIn()
summarizer = Summarizer()
ytSummarizer = YouTubeTranscriptSummarizer()
twitter = Twitter()
discord = Discord()
youtube_upload = YouTubeUploader(title_description)
# app = WorkFlow().app
# app.invoke({})

class SocialMediaScheduler:
    def extract_feat(self,statement:str):
        platform_pattern = re.compile(r'\b(instagram|twitter|discord|facebook|linkedin|youtube)\b', re.IGNORECASE)
        time_pattern = re.compile(r'\bat\s+(\d{1,2}(?::\d{2})?\s?(?:am|pm)?)\s*(today|now|tomorrow|next\s(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday))?\b', re.IGNORECASE)
        content_pattern = re.compile(r'content\s+["“](.*?)["”]', re.IGNORECASE)
        alternative_content_pattern = re.compile(r'''["“'](.*?)['"”]''', re.IGNORECASE)
        
       
        platform_match = platform_pattern.search(statement)
        time_match = time_pattern.search(statement)
        content_match = content_pattern.search(statement)
        alternative_content_match = alternative_content_pattern.search(statement)

        
        platform = platform_match.group(1) if platform_match else None
        time = time_match.group(1) if time_match else None
        day_context = time_match.group(2) if time_match else None
        content = content_match.group(1) if content_match else (alternative_content_match.group(1) if alternative_content_match else None)
        if time == None and day_context == None: 
            full_date=None
        elif time==None:
            full_date=day_context
        elif day_context==None:
            full_date=time
        else:
            full_date=time+day_context
        
        dicto=[platform,full_date,content]  
        return dicto
    
    def schedule_post(self, platform: str, datetime_str: str, content: str):
        post_time = self.parse_time(datetime_str)
        current_time = datetime.now()

        delay = ((post_time - current_time).total_seconds())-60
        if delay > 0:
            time.sleep(delay)

        self.post_content(platform, content)

    def parse_time(self, time_str: str) -> datetime:
        current_time = datetime.now()
        if time_str!=None:
            time_str = time_str.lower()

            if "today" in time_str:
                time_part = parser.parse(time_str.replace("today", "").strip(), default=current_time)
                post_time = current_time.replace(hour=time_part.hour, minute=time_part.minute, second=0, microsecond=0)
            # elif time_str=None:
                
            elif "tomorrow" in time_str:
                time_part = parser.parse(time_str.replace("tomorrow", "").strip(), default=current_time)
                post_time = (current_time + relativedelta.relativedelta(days=1)).replace(hour=time_part.hour, minute=time_part.minute, second=0, microsecond=0)
            
            elif "next" in time_str:
                time_part = parser.parse(time_str)
                post_time = current_time + relativedelta.relativedelta(weekday=time_part.weekday(), hour=time_part.hour, minute=time_part.minute, second=0, microsecond=0)
                if post_time <= current_time:
                    post_time += relativedelta.relativedelta(weeks=1)
            
            else:
                post_time = parser.parse(time_str, default=current_time)
                
        else:
            post_time=current_time
            
        return post_time

    def post_content(self, platform: str, content: str):
        platform = platform.lower()
        if platform == "instagram":
            self.post_to_instagram(content)
        elif platform == "facebook":
            self.post_to_facebook(content)
        elif platform == "discord":
            self.post_to_discord(content)
        elif platform == "linkedin":
            self.post_to_linkedin(content)
        elif platform == "twitter":
            self.post_to_twitter(content)
        elif platform == "youtube":
            self.post_to_youtube(content)
        else:
            print("Unsupported platform")

    def post_to_instagram(self, content: str):
        instagram.run(content)

    def post_to_facebook(self, content: str):
        facebook.run(content)

    def post_to_discord(self, content: str):
        discord.run(content)
        
    def post_to_linkedin(self, content: str):
        linkedin.run(content)
    
    def post_to_twitter(self, content: str):
        twitter.run(content)

    def post_to_youtube(self,video_path:str):
        video_path = input("video link : ")
        youtube_upload.upload(video_path)


scheduler = SocialMediaScheduler()
while True:
    state = input("enter: ")
    # input_stat="I need you to review the document now, but post the content 'Big sale coming up!' on instagram  at 9:26AM "  
    platform,date,content=scheduler.extract_feat(statement=state)
    scheduler.schedule_post(platform=platform, datetime_str=date,content=content)

