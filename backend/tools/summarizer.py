from langchain.tools import BaseTool
from langchain_openai import OpenAI  # Updated import path
import os
from typing import Optional

class SummarizerTool(BaseTool):
    name: str = "summarizer"
    description: str = "Summarize text."
    llm: Optional[OpenAI] = None

    def __init__(self):
        super().__init__()
        self.llm = OpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

    def _run(self, text: str) -> str:
        prompt = f"Please provide a concise summary of the following text:\n\n{text}"
        summary = self.llm(prompt)
        return summary.strip()

    async def _arun(self, text: str) -> str:
        raise NotImplementedError("Async not implemented for SummarizerTool.")
