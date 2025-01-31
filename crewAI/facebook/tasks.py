# Import necessary modules and classes
from agents import (
    facebook_drafting_agent,
    facebook_refinement_agent,
    facebook_seo_agent,
    facebook_content_compiler, 
)
from crewai import Task
drafting_task_facebook = Task(
    description=(
        "Generate a draft for a Facebook post on {topic}. "
        "Create content that is informative, engaging, and aligns with current trends or developments in {topic}. "
        "Include a mix of text and ideas for multimedia elements (like images, videos, or links) to enhance the post's engagement."
    ),
    expected_output=(
        "A compelling draft Facebook post on {topic}, capturing the essence of {topic} and resonating with Facebook users. "
        "The draft should include suggestions for multimedia elements that support the content and enhance its appeal."
    ),
    agent=facebook_drafting_agent,
)

editing_task_facebook = Task(
    description=(
        "Refine and polish a draft Facebook post on {topic}. "
        "Focus on enhancing grammar, clarity, and overall readability while ensuring alignment with the intended style and engagement goals. "
        "Ensure the content is structured to maximize readability and interaction, and consider the inclusion of appropriate media."
    ),
    expected_output=(
        "A polished Facebook post on {topic}, improved in grammar, clarity, and readability. "
        "The post effectively communicates the intended message while maintaining a style that resonates with Facebook users. "
        "The content should be engaging and ready for integration with multimedia elements."
    ),
    agent=facebook_refinement_agent,
)

seo_task_facebook = Task(
    description=(
        "Optimize a Facebook post on {topic} for discoverability and engagement. "
        "Identify and integrate relevant keywords and tags to improve visibility on Facebook's platform. "
        "Consider the use of effective SEO strategies to enhance the post's reach and engagement."
    ),
    expected_output=(
        "An optimized Facebook post on {topic}, enhanced with relevant keywords and tags. "
        "The post is structured to maximize discoverability and engagement, appealing to the target audience effectively. "
       
    ),
    agent=facebook_seo_agent,
)

chief_task_facebook = Task(
    description=(
        "Aggregate and compile the final results from various tasks into a cohesive Facebook post. "
        "Integrate content generated by drafting, refinement, SEO optimization into a unified and engaging presentation."
    ),
    expected_output=(
        "A finalized Facebook post on {topic}, incorporating outputs from drafting, refinement, SEO optimization. "
        "The post should be engaging, visually appealing, and tailored to resonate with the target audience on Facebook. "
        "End the post with a call-to-action inviting viewers to engage with the content, such as commenting, sharing, or clicking a link."
    ),
    agent=facebook_content_compiler,
    async_execution=False,
    output_file="outputs/facebook/post.md"
)

