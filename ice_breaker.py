import os 
from dotenv import load_dotenv

from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from third_parties.linkedin import scrape_linkedin_profile

if __name__ == "__main__":
  load_dotenv()

  # variables inside of curly brackets represent parameters 
  summary_template = """
    given the Linkedin information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
  """

  # information to be used as a variable 
  linkedin_information = scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/owenwang05/", mock=True)

  # create a prompt template object 
  summary_prompt_template = PromptTemplate(template=summary_template, input_variables=["information"])

  # creates a wrapper around gpt model (temperature = creativeness)
  llm = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"], temperature=0, model_name="gpt-3.5-turbo")

  # uses langchain expression language to send prompt to llm to output parser
  chain = summary_prompt_template | llm | StrOutputParser()

  # run chain 
  res = chain.invoke(input={"information": linkedin_information})
  
  print(res)
