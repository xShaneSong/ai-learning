from langchain_ollama.chat_models import ChatOllama
from langchain.prompts import (
    ChatPromptTemplate, # 用于构建聊天提示模板
    HumanMessagePromptTemplate, # 用于构建人类消息提示模板
    SystemMessagePromptTemplate,# 用于构建系统消息提示模板
)

chat = ChatOllama(model="qwen3:8b", max_tokens=256, verbose=True)

template = "你是一个翻译助理，请将用户输入 的内容由{input_language}翻译为{output_language}。"
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

print(chat.invoke(chat_prompt.format_messages(input_language="中文", output_language="英文", text="今天天气很好。")))

