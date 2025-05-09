from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_ollama.chat_models import ChatOllama
from langchain.agents import initialize_agent, AgentType
# from langchain.langgraph import ReActAgent
from langchain.callbacks.streaming_stdout_final_only import FinalStreamingStdOutCallbackHandler

tools = [TavilySearchResults(max_results=1)]

# llm = ChatOllama(model="qwen3:8b", max_tokens=256, temperature=0, verbose=True)
llm = ChatOllama(model="qwen3:8b",
                 max_tokens=256,
                 temperature=0,
                 verbose=True,
                 streaming=True,
                 callbacks=[FinalStreamingStdOutCallbackHandler()]
                 )

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "你是一位很有帮助的助手。请确保使用tavily_search_results_json工具来获取相关信息"
        ),
        ("placeholder", "{chat_history}"),
        HumanMessagePromptTemplate.from_template("{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

def _handle_tool_errors(e: Exception) -> str:
    """
    自定义错误处理函数
    """
    return f"自定义错误处理: {str(e)}"

# 使用 initialize_agent 创建代理
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # 使用零样本反应式代理
    verbose=True,
    prompt=prompt,
    # handle_parse_errors=True, #默认错误处理
#    handle_tool_errors="自定义错误处理", #自定义错误处理
    _handle_tool_errors=_handle_tool_errors, #自定义错误处理
    return_intermediate_steps=True,  # 返回中间步骤

)

# # Create a ReAct agent using LangGraph
# agent_executor = ReActAgent(
#     llm=llm,
#     tools=tools,
#     prompt=prompt,
#     verbose=True,
# )

# agent = create_tool_calling_agent(llm, tools, prompt)
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
agent_executor.invoke({"input": "whiat is langchain?"})
