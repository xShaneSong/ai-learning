import os

if not os.getenv("DEEPSEEK_API_KEY"):
    os.environ["DEEPSEEK_API_KEY"] = getpass.getpass("请输入您的 DeepSeek API 密钥: ")


from langchain_deepseek import ChatDeepSeek
from langchain.schema import (
    AIMessage,
    BaseMessage,
    ChatMessage,
    HumanMessage,
    SystemMessage,
)

llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # 其他参数...
)

# messages = [
#     (
#         "system",
#         "您是一个有用的助手，负责将中文翻译成日文。请翻译用户句子。",
#     ),
#     ("human", "我喜欢编程。"),
# ]

messages = [
    SystemMessage(
        content="You are a helpful assistant that translates Chinese to Japanese. Please translate the user's sentence."
    ),
    HumanMessage(content="我喜欢编程。"),
]
ai_msg = llm.invoke(messages)
print(ai_msg.content)

messages_gen = [
    [
        SystemMessage(
            content="You are a helpful assistant that translates Chinese to Japanese. Please translate the user's sentence."
        ),
        HumanMessage(content="我喜欢编程。"),
    ]
]
result = llm.generate(messages_gen)
print(result)