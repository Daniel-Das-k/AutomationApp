import os
from crewai import Agent
from .tools.search_tools import search_tool
from .tools.trends_tools import TrendsTools
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()


llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
									verbose=True,
									temperature=0.5,
									google_api_key=os.getenv("GOOGLE_API_KEY"))

# groq_api_key = os.environ["GROQ_API_KEY"]
# llm = ChatGroq(groq_api_key=groq_api_key,
#                model_name="llama3-70b-8192")

trending_topic_researcher_agent = Agent(
		role="Trending Topic Researcher",
		goal=("""\
			Identify and compile a list of current trending topics and searches
			within a specific niche. This list should provide actionable insights
			and opportunities for strategic engagement, helping to guide content
			creation."""),
		backstory=("""\
			As a Trending Topic Researcher at a cutting-edge digital
			marketing agency, your primary responsibility is to monitor and
			decode the pulse of the market. Using advanced analytical tools,
			you uncover and list the most relevant trends that can influence
			strategic decisions in content creation."""),
		tools=[
				TrendsTools.trending_searches_on_google,
				search_tool
		],
		allow_delegation=False,
		llm=llm,
		verbose=True
	)


content_researcher_agent = Agent(
		role="Content Researcher",
		goal=("""\
			Conduct in-depth research on a topic and compile
			detailed, useful information and insights for each topic. This
			information should be actionable and suitable for creating engaging
			and informed social media posts."""),
		backstory=("""\
			As a Content Researcher at a dynamic social media marketing agency,
			you delve deeply into trending topics to uncover underlying themes and
			insights. Your ability to discern and utilize authoritative and relevant
			sources ensures the content you help create resonates with audiences and
			drives engagement."""),
		tools=[
			search_tool
		],
		llm=llm,
		verbose=True
	)


creative_content_creator_agent = Agent(
		role="Twitter Content Creator",
		goal=("""\
			Develop compelling and innovative content
			for social media campaigns, with a focus on creating
			high-impact Twitter tweet copies. Make sure you don't use tools with the same arguments twice.
			Make sure not to do more than 3 google searches."""),
		backstory=("""\
			As a Creative Content Creator at a top-tier
			digital marketing agency, you excel in crafting narratives
			that resonate with audiences on social media.
			Your expertise lies in turning marketing strategies
			into engaging stories and visual content that capture
			attention and inspire action."""),
		tools=[
			search_tool
		],
		llm=llm,
		verbose=True
	)