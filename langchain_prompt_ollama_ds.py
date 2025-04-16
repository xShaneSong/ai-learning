from langchain_ollama import OllamaLLM

#创建Ollama实例
llm = OllamaLLM(
    model="deepseek-r1:7b",  # 替换为实际模型名称
    base_url='http://localhost:11434',  # 本地Ollama服务地址
    #temperature=0.7,       # 控制生成随机性（0-1）
    # num_ctx=2048        # 上下文长度
)

# # 调用模型生成响应
# response = llm.invoke("In which country is beijing?")
# print(response)

# 使用流式响应（适合长文本）
# for chunk in llm.stream("如何制作一杯好的绿茶？步骤："):
#     print(chunk, end="", flush=True)

#########################
# from langchain_core.messages import HumanMessage, SystemMessage

# messages = [
#     HumanMessage(content="Say 'hello world' in Python."),
#     SystemMessage(content="You are a helpful assistant that translates natural language to Python code."),
# ]
# print(llm.invoke(messages))

########################
prompt = """
Summarize this text in one sentence:

{text}
"""
# print(llm.invoke(prompt.format(text="The quick brown fox jumps over the lazy dog.")))
####################

# from langchain_core.prompts import PromptTemplate
# prompt_template = PromptTemplate.from_template("Tell me a {adjective} joke about {topic}.")
# prompt_value = prompt_template.invoke({"adjective":"funny", "topic":"cats"})
# print(llm.invoke(prompt.format(text=prompt_value)))

####################
from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "What is the capital of France?"),
    ("assistant", "The capital of France is Paris."),
])
print(llm.invoke(template.format_messages()))