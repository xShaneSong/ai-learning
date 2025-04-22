from langchain.tools import tool

@tool
def get_weather(location: str) -> str:
    """
    Get weather of a location. The user should supply a location first.
    """
    if "Dalian" == location:
        return f"The weather in {location} is 30℃."
    if "dalian" in location.lower():
        return f"The weather in {location} is 24℃."
    elif location.lower() == "beijing":
        return f"The weather in {location} is 20℃."
    else:
        return f"The weather in {location} is unknown."
    
from langchain.agents import initialize_agent, Tool

# 定义工具
tools = [
    Tool(
        name="GetWeather",
        func=get_weather,
        description="Get the weather for a given location."
    )
]

# 初始化代理
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-chat",  # 指定 DeepSeek 支持的模型
    temperature=0,
    openai_api_key="{api-key}",  # 替换为你的 DeepSeek API 密钥
    openai_api_base="https://api.deepseek.com/v1"  # DeepSeek 的 API 基础地址
)
agent = initialize_agent(tools,
                        llm,
                        agent="zero-shot-react-description",
                        verbose=True,
                        handle_parsing_errors=True,
                        max_iterations=3)

# 使用代理
response = agent.run("What is the weather in dalian?")
print(response)