from typing import Optional, Type
from pydantic import Field, BaseModel
from langchain.tools import StructuredTool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun, CallbackManagerForToolRun,
)
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType

def get_weather(query: str) -> str:
    """Get the weather for a given location."""
    print(f"Running tool with query: {query}")
    if "Dalian" == query:
        print("Query matches Dalian")
        return f"The weather in {query} is 30℃."
    if "dalian" in query.lower():
        print("Query contains 'dalian'")
        return f"The weather in {query} is 24℃."
    elif query.lower() == "beijing":
        return f"The weather in {query} is 20℃."
    else:
        return f"The weather in {query} is unknown."
    
# get_weather_tool = StructuredTool.from_function(
#     func=get_weather,
#     name="GetWeather",
#     description="Get the weather for a given location.",
# )

class GetWeather(BaseModel):
    query: str = Field(description="The location to get the weather for.")

# Define the tool using StructuredTool
class GetWeatherTool(StructuredTool):
    name: str = "GetWeather"  # Use a regular string assignment
    description: str = "Get the weather for a given location."  # Use a regular string assignment
    args_schema: Type[BaseModel] = GetWeather

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """Use the tools."""
        return get_weather(query)

    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """Use the tools asynchronously."""
        raise NotImplementedError("GetWeather does not support async")

get_weather_tool = GetWeatherTool()

# Wrap the tool in a LangChain Tool object
tool = Tool(
    name=get_weather_tool.name,  # Access the instance attribute
    func=get_weather_tool._run,  # Access the instance method
    description=get_weather_tool.description,  # Access the instance attribute
)

llm = ChatOpenAI(
    model="deepseek-chat",  # 指定 DeepSeek 支持的模型
    temperature=0,
    openai_api_key="{api-key}",  # 替换为你的 DeepSeek API 密钥
    openai_api_base="https://api.deepseek.com/v1"  # DeepSeek 的 API 基础地址
)
agent = initialize_agent(tools=[tool],
                        llm=llm,
                        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                        verbose=True,
                        handle_parsing_errors=True,
                        max_iterations=3)

# 使用代理
response = agent.run("What is the weather in Dalian?")
print(response)