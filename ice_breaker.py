import os 
from dotenv import load_dotenv

load_dotenv()

from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parsers import summary_parser
from output_parsers import Summary
from typing import Tuple

def ice_break_with(name: str) -> Tuple(Summary, str):
  linkedin_profile_url = linkedin_lookup_agent(name=name)

  # variables inside of curly brackets represent parameters 
  summary_template = """
    given the Linkedin information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them

    \n{format_instructions}
  """

  # information to be used as a variable 
  linkedin_information = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url, mock=True)

  # create a prompt template object 
  summary_prompt_template = PromptTemplate(template=summary_template, input_variables=["information"], partial_variables={"format_instructions": summary_parser.get_format_instructions()})

  # creates a wrapper around gpt model (temperature = creativeness)
  llm = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"], temperature=0, model_name="gpt-3.5-turbo")

  # uses langchain expression language to send prompt to llm to output parser
  chain = summary_prompt_template | llm | summary_parser

  # run chain 
  res:Summary = chain.invoke(input={"information": linkedin_information})
  
  # print(res)

  return (res, linkedin_information.get("profile_pic_url"))


if __name__ == "__main__":
  ice_break_with("owen wang uiuc")

