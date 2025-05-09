from langchain.agents import AgentExecutor, Tool, create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_ollama.chat_models import ChatOllama
from langchain.agents import initialize_agent, AgentType

# Define core tools
def web_search(query: str) -> str:
    """Simulate a web search tool."""
    return "Relevant data: China's Q1 2025 GDP grew by 5.3%."

def data_analysis(query: str) -> str:
    """Simulate a data analysis tool."""
    return "Analysis result: Economic indicators are in line with expectations."

class ReportGenerator:
    @staticmethod
    def generate_report(content: str) -> str:
        """Report generation tool."""
        return f"Formal Report:\n# Economic Analysis\n{content}\nGenerated on: 2025-05-09"

# Initialize LLM
llm = ChatOllama(model="qwen3:8b", max_tokens=256, temperature=0, verbose=True)

# Define tools
tools = [
    Tool(name="WebSearch", func=web_search, description="Use for accessing the latest economic data."),
    Tool(name="DataAnalysis", func=data_analysis, description="Use for performing numerical analysis."),
    Tool(name="ReportGeneration", func=ReportGenerator.generate_report, description="Use for generating formal documents."),
]

# Build prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", """作为经济分析师，请按以下流程工作：
1. 明确用户需求
2. 收集必要数据
3. 执行深度分析
4. 生成结构化报告

可用工具：
{tool_names}

工具描述：
{tools}
"""),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
    # MessagesPlaceholder(variable_name="chat_history"),  # Placeholder for conversation history
    # ("human", "{input}"),
    # MessagesPlaceholder(variable_name="agent_scratchpad")  # Placeholder for intermediate steps
])

# # Configure memory
# memory = ConversationBufferMemory(
#     memory_key="chat_history",
#     return_messages=True
# )

# # Create agent executor
# agent = create_react_agent(llm, tools, prompt)
# agent_executor = AgentExecutor(
#     agent=agent,
#     tools=tools,
#     # memory=memory,  # Attach memory to manage chat_history
#     verbose=True,
#     max_iterations=5
# )

agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # 使用零样本反应式代理
    verbose=True,
    prompt=prompt,
)

# Execute example
response = agent_executor.invoke({
    "input": "请生成最新中国经济形势分析报告"
})
print("\n最终输出：\n" + response["output"])
