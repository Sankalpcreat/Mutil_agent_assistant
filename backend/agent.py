from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import OpenAI  # Updated import path
from tools.websearch import WebSearchTool
from langchain.prompts import PromptTemplate  
from tools.fetch_weather import FetchWeatherTool
from tools.summarizer import SummarizerTool
import os

def create_agent():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    
    # Initialize the language model
    llm = OpenAI(temperature=0, openai_api_key=openai_api_key)

    # Define the tools
    tools = [WebSearchTool(), FetchWeatherTool(), SummarizerTool()]

    # Define the prompt template with required input variables
    template = '''Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought:{agent_scratchpad}'''

    # Create the PromptTemplate object
    prompt = PromptTemplate.from_template(template)

    # Create the ReAct agent
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt,
    )

  
    agent_executor = AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True)
    return agent_executor