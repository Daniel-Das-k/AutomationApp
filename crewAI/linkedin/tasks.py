
from agents import drafting_agent, seo_optimization_agent, editing_refinement_agent, content_formater_agent,image_generator_agent,chief_agent
from crewai import Task

drafting_task = Task(
    description=(
        "Generate a draft on {topic} for a LinkedIn post. "
        "Focus on creating content that is informative, engaging, and aligned with current trends or developments in {topic}."
    ),
    expected_output=(
        "A compelling draft LinkedIn post on {topic}, capturing the essence of {topic} and resonating with the target audience on LinkedIn."
    ),
    agent=drafting_agent,
)

editing_task = Task(
    description=(
        "Refine and polish a draft LinkedIn post on {topic}. "
        "Focus on improving grammar, clarity, and overall readability while ensuring alignment with brand voice and objectives. "
        "Add relevant emojis in a professional way."
    ),
    expected_output=(
        "A polished LinkedIn post on {topic}, enhanced in grammar, clarity, and readability. "
        "The post effectively communicates the intended message while maintaining consistency with brand guidelines."
    ),
    agent=editing_refinement_agent,
)

seo_task = Task(
    description=(
        "Optimize a LinkedIn post on {topic} for searchability and discoverability. "
        "Identify and integrate relevant keywords and hashtags to improve visibility on LinkedIn’s platform."
    ),
    expected_output=(
        "An optimized LinkedIn post on {topic}, improved with relevant keywords and hashtags. "
        "The post is structured to enhance search engine visibility and attract the target audience effectively."
    ),
    agent=seo_optimization_agent,
)

chief_task = Task(
    description=(
        "Aggregate and compile the final results from various tasks into a cohesive LinkedIn post. "
        "Integrate content generated by drafting, refinement, SEO optimization into a unified presentation."
    ),
    expected_output=(
        "A finalized LinkedIn post on {topic}, incorporating outputs from drafting, refinement, SEO optimization,. "
        "The post is engaging, informative, and tailored to resonate with the target audience on LinkedIn. "
        "End the post with an interactive call-to-action inviting readers to share their thoughts or comments below."
    ),
    agent=chief_agent,
    
)

image_generate_task = Task(
    description=(
        "Create 5 images that capture and enhance the essence of a LinkedIn post about {topic}. "
        "Each image should be relevant to the content of the post, reflecting the professional tone of LinkedIn. "
        "The images should add visual appeal and help convey the message effectively to engage a professional audience."
        """Imagine what the photo you wanna take describe it in a paragraph.
			Here are some examples for you to follow:
			- high tech airplaine in a beautiful blue sky in a beautiful sunset super cripsy beautiful 4k, professional wide shot
			- the last supper, with Jesus and his disciples, breaking bread, close shot, soft lighting, 4k, crisp
			- an bearded old man in the snows, using very warm clothing, with mountains full of snow behind him, soft lighting, 4k, crisp, close up to the camera

			Think creatively and focus on how the image can capture the audience's
			attention."""

    ),
    agent=image_generator_agent,
    expected_output=(
        "An image that visually represent and complement the LinkedIn post on {topic}. "
        "The image should be professional, engaging, and aligned with LinkedIn's aesthetic and tone. "
        "Your final answer must be 3 options of photographs, each with 1 paragraph describing the photograph exactly like the examples provided above."
    ),
)

format_content_task = Task(
    description='Format the linkedin content in markdown, including an image at the end of the linkedin post.',
    agent=content_formater_agent,
    expected_output='The entire post content formatted in markdown, with content on the beginning and choose one of the description among the description of the image content generated and attach it to the end of the post content.',
    context=[chief_task, image_generate_task],
    async_execution=False,
    output_file="outputs/linkedin/post.md"
)
