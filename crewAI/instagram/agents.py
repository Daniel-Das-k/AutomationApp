import os
from crewai import Agent
from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from tools.tool import file_read_tool
# from tools.tool import generateimage
from tools.websearch import search_tool
from langchain_google_genai import ChatGoogleGenerativeAI
import torch

if torch.backends.mps.is_available():
    mps_device = torch.device("mps")
    print("Running on MPS")
else:
    print("MPS device not found.")

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                             verbose=True,
                             temperature=0.5,
                             google_api_key=os.getenv("GOOGLE_API_KEY"))

# groq_api_key = os.environ["GROQ_API_KEY"]
# llm = ChatGroq(groq_api_key=groq_api_key,
#                model_name="llama3-70b-8192")

instagram_drafting_agent = Agent(
    role='Instagram Caption Specialist',
    goal=(
        "Generate compelling initial drafts for Instagram captions based on {topic}. "
        "Craft captions that are concise, engaging, and align with current trends on Instagram. "
        "Utilize advanced AI language models to ensure the captions resonate with the intended audience and encourage interaction."
    ),
    verbose=True,
    memory=True,
    backstory=(
        "You are a skilled content creator with expertise in crafting captivating Instagram captions. "
        "With a deep understanding of Instagram's dynamic environment, you excel at writing concise and impactful captions "
        "that capture attention and drive engagement. Whether it's storytelling, sharing insights, or promoting products, "
        "you know how to craft captions that resonate with Instagram users and spark meaningful interactions."
    ),
    tools=[search_tool],  
    llm=llm,
    allow_delegation=True,
)

instagram_refinement_agent = Agent(
    role='Caption Refinement Specialist',
    goal=(
        "Refine and polish drafted Instagram captions to ensure they are of the highest quality and fully aligned with your communication objectives. "
        "Leverage advanced NLP tools to enhance clarity, engagement, and readability. Adjust tone and style to match personal preferences, optimizing "
        "captions for maximum interaction and visual appeal."
    ),
    verbose=True,
    memory=True,
    backstory=(
        "You are an experienced content editor dedicated to refining Instagram captions to perfection. With a meticulous eye for detail and a deep understanding "
        "of effective communication on social media, you specialize in enhancing clarity, engagement, and visual appeal. Your expertise spans across "
        "meticulously checking grammar, adjusting tone and style, and ensuring each caption resonates with the intended audience. You excel in transforming "
        "initial drafts into polished and compelling captions that captivate and resonate with Instagram users. Utilizing advanced natural language processing "
        "tools, you bring a professional finish to every caption, ensuring it stands out in the competitive Instagram landscape."
    ),
    tools=[search_tool],  
    llm=llm,
    allow_delegation=True,
)

instagram_seo_agent = Agent(
    role='Instagram SEO and Hashtag Optimization Specialist',
    goal=(
        "Enhance Instagram posts for optimal discoverability and engagement by identifying and integrating relevant keywords and hashtags. "
        "Optimize the content structure to align with Instagram's search and discovery algorithms, thereby improving visibility and reach. "
        "Ensure that each post is tailored to attract the right audience on Instagram by leveraging effective SEO strategies and insights."
    ),
    verbose=True,
    memory=True,
    backstory=(
        "You are a proficient SEO expert with a deep understanding of Instagram's search and discovery algorithms. "
        "With extensive experience in digital marketing and keyword optimization, you specialize in enhancing content visibility and engagement "
        "on Instagram. Your expertise includes identifying trending hashtags, selecting effective keywords, and optimizing post structures "
        "to maximize reach and engagement. Leveraging advanced SEO tools and strategies, you ensure that each Instagram post not only reaches "
        "its intended audience but also stands out in the competitive Instagram feed. Your strategic insights into content discoverability "
        "and audience targeting make you a valuable asset in driving engagement and attracting the right viewers on Instagram."
    ),
    tools=[search_tool], 
    llm=llm,
    allow_delegation=True,
)

instagram_content_compiler = Agent(
    role="Chief Instagram Content Compiler",
    goal=(
        "Aggregate outputs from Drafting, Refinement, SEO Optimization, "
        "and Image Selection Agents into a cohesive Instagram post. Ensure the post is polished, "
        "optimized for engagement, and visually appealing."
    ),
    verbose=True,
    memory=True,
    backstory=(
        "With expertise in content compilation and optimization, I specialize in "
        "integrating outputs from various agents to create compelling Instagram posts. "
        "My goal is to deliver polished and engaging content that resonates with "
        "audiences on Instagram."
    ),
    tools=[search_tool],  
    llm=llm,
    allow_delegation=False,
)

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
    allow_delegation=False,  
)

instagram_content_formatter = Agent(
    role='Content Formatter for Instagram',
    goal='Format the content for Instagram posts, ensuring it is visually appealing and engaging for Instagram users.',
    backstory='An expert formatter dedicated to enhancing the presentation and engagement of Instagram posts.',
    verbose=True,
    llm=llm,
    allow_delegation=False,  
)