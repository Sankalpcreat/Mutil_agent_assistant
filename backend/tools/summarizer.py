from langchain.tools import BaseTool
from langchain.llms import OpenAI
import os

class SummarizerTool(BaseTool):
    name="summarizer"
    description="Summarize Text."

def __init__(self):
    super().__init__()
    self.llm = OpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

def _run(self,text:str):
   
   prompt = f"Please provide a concise summary of the following text:\n\n{text}"
   summary=self.llm(prompt)
   return summary.strip()


async def _arun(self, text: str):
    raise NotImplementedError("Async not implemented for SummarizerTool.")
