from langchain.tools import tool

@tool
def get_weather(location: str) -> str:
    """
    Get weather of a location. The user should supply a location first.
    """

    print(f"get_weather: {location}")
    if "Dalian" == location:
        return f"The weather in {location} is 30℃."
    if "dalian" in location.lower():
        return f"The weather in {location} is 24℃."
    elif location.lower() == "beijing":
        return f"The weather in {location} is 20℃."
    else:
        return f"The weather in {location} is unknown."
    
from langchain.agents import initialize_agent, Tool, AgentType

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
from langchain_ollama import OllamaLLM

llm = OllamaLLM(
    model="deepseek-r1:7b",  # 替换为实际模型名称
    base_url='http://localhost:11434',  # 本地Ollama服务地址
    #temperature=0.7,       # 控制生成随机性（0-1）
    # num_ctx=2048        # 上下文长度
)
agent = initialize_agent(tools,
                        llm,
                        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                        verbose=True,
                        handle_parsing_errors=True,
                        max_iterations=3)

# 使用代理
response = agent.run("What is the weather in dalian?")
print(response)