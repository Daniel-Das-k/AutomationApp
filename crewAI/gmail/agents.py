from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
import os
# from gemini_functions_agent import agent_executor as gemini_functions_agent_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import hub
from langchain.agents import AgentType, initialize_agent
toolkit = GmailToolkit()

credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="credentials.json",
)
api_resource = build_resource_service(credentials=credentials)
toolkit = GmailToolkit(api_resource=api_resource)

tools = toolkit.get_tools()
print(tools)


llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                             verbose=True,
                             temperature=0.5,
                             google_api_key=os.getenv("GOOGLE_API_KEY"))

agent = initialize_agent(llm, toolkit.get_tools(),agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                         )


agent.invoke(
    {
         "Create a gmail draft for me to edit of a letter from the perspective of a sentient parrot"
        " who is looking to collaborate on some research with her"
        " estranged friend, a cat. Under no circumstances may you send the message, however."
    }
)