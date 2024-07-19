from crewAI.email.src.graph import WorkFlow
from crewAI.facebook.crew import Facebook
from crewAI.instagram.crew import Instagram
from crewAI.linkedin.crew import LinkedIn
from crewAI.twitter.twitter import TwitterAutoPoster
from crewAI.summarization.summarize import Summarizer
from crewAI.yt_summarizer.ytTransSummarizer import YouTubeTranscriptSummarizer
from voice import VoiceAssistant

voice_assistant = VoiceAssistant()
facebook = Facebook(voice_assistant)
instagram = Instagram(voice_assistant)
linkedin = LinkedIn(voice_assistant)
summarizer = Summarizer(voice_assistant)
ytSummarizer = YouTubeTranscriptSummarizer()
twitter = TwitterAutoPoster()
# app = WorkFlow().app
# app.invoke({})

def Automation():
    while True:
        # voice_assistant.speak("Listening")
        # query = voice_assistant.get_audio()
        query = input(": ")

        if "linkedin" in query.lower():
            linkedin.run()

        elif "instagram" in query.lower():
            instagram.run()

        elif "facebook" in query.lower():
            facebook.run()
        
        elif "twitter" in query.lower():
            twitter.run()

        elif "summarise" in query.lower():
            summarizer.run()

        elif "youtube summarizer" in query.lower():
            voice_assistant.speak("Enter YouTube Video Link: ")
            youtube_link = input(": ")
            if youtube_link:
                ytSummarizer.process_video(youtube_link)

        else:
            voice_assistant.speak("Sorry currently unavailable")






