from langchain_community.chat_models import ChatOllama
from langchain.prompts.chat import (
    ChatPromptTemplate, # 用于构建聊天指令模板的基类
    SystemMessagePromptTemplate, # 用于构建系统消息的指令模板
    HumanMessagePromptTemplate, # 用于构建人类消息的指令模板
    AIMessagePromptTemplate, # 用于构建AI消息的指令模板
)

# llm_qwen3 = OllamaLLM(model = "qwen3:1.7b")
llm_ds15 = OllamaLLM(model = "deepseek-r1:1.5b")
llm_ds8 = OllamaLLM(model = "deepseek-r1:8b")
print(llm_ds15.invoke("What is the capital of France?"))