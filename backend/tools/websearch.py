from langchain.tools import BaseTool
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
import asyncio

class WebSearchTool(BaseTool):
    name:str = "web_search"
    description:str = "Perform a web search and retrieve information."

    def _run(self, query: str) ->str:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=5)
            if not results:
                return "No results found."
            summaries = [BeautifulSoup(result['body'], 'html.parser').get_text() for result in results]
            return "\n\n".join(summaries)

    async def _arun(self, query: str)->str:
        async with DDGS() as ddgs:
            results = [result async for result in ddgs.text(query, max_results=5)]
            if not results:
                return "No results found."
            summaries = [BeautifulSoup(result['body'], 'html.parser').get_text() for result in results]
            return "\n\n".join(summaries)
