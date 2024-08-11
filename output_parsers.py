from typing import List, Dict, Any
from langchain.output_parsers import PydanticOutputParser # define schemas and validate inputs against schemas 
from langchain_core.pydantic_v1 import BaseModel, Field 

class Summary(BaseModel):
  # create fields
  summary: str = Field(description="summary")
  facts: List[str] = Field(description="intersting facts about them")

  # create serializer
  def to_dict(self) -> Dict[str, Any]:
    return {"summary": self.summary, "facts": self.facts}
  
summary_parser = PydanticOutputParser(pydantic_object=Summary)