from typing import List

from pydantic import BaseModel, Field
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

load_dotenv()

class Source(BaseModel):
    """Scheme for a source used by the agent"""

    url:str = Field(description="The URL of the source used by the agent")


class AgentResponse(BaseModel):
    """Scheme for agent response witht answer and sources returned by the agent"""

    answer: str = Field(description="The agent's answer to the query")
    sources: List[Source] = Field(default_factory=list, description="The list of sources used by the agent to generate the answer.")

llm = ChatOpenAI(model="gpt-5")
tools = [TavilySearch()]
agent = create_agent(model=llm, tools=tools, response_format=AgentResponse)


def main():
    print("Hello from langchain-course!")
    result = agent.invoke(
        {
            "messages": [HumanMessage(
                content="search for 3 job postings in the last 24 hours for a devops engineer in Canada on Linkedin!")]
        }
    )
    print(result)
    

if __name__ == "__main__":
    main()
