import os 
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
  create_react_agent,
  AgentExecutor
)
from langchain import hub

from tools.tools import get_profile_url_tavily

def lookup(name: str) -> str:

  llm = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"], temperature=0, model_name="gpt-3.5-turbo")

  template = """
    Given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page.
    Your answer should contain only a linkedin URL"""

  prompt_template = PromptTemplate(template=template, input_variables=["name_of_person"])

  # create available tools for the agent 
  tools_for_agent = [
    Tool(
      name="Crawl Google 4 linkedin profile page",
      func=get_profile_url_tavily,
      description="useful for when you need to get the linkedin page URL"
    )
  ]

  # pull react prompt from langchain hub 
  react_prompt = hub.pull("hwchase17/react")

  # create agent
  agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)

  # create agent executor (agent runtime)
  agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

  # invoke the agent 
  result = agent_executor.invoke(
    input={"input": prompt_template.format_prompt(name_of_person=name)}
  )
  
  linkedin_profile_url = result["output"]

  return linkedin_profile_url

if __name__ == "__main__":
  lookup("owen wang uiuc")