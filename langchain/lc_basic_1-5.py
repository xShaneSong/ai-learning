from langchain_ollama.chat_models import ChatOllama
from langchain.prompts import (
    ChatPromptTemplate, # 用于构建聊天提示模板
    HumanMessagePromptTemplate, # 用于构建人类消息提示模板
    SystemMessagePromptTemplate,# 用于构建系统消息提示模板
)

from langchain.globals import set_debug, set_verbose
# 设置调试和详细输出
set_debug(True)
set_verbose(True)


template = "你是一个翻译助理，请将用户输入 的内容由{input_language}翻译为{output_language}。"
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

from langchain_openai import ChatOpenAI
import os
from unittest.mock import patch

os.environ["OPENAI_API_KEY"] = "sk-xxxxxx"
os.environ["OPENAI_API_BASE"] = "https://api.openai.com/v1"


from typing import Any, Dict, List
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.outputs import LLMResult
class LoggingHandler(BaseCallbackHandler):
    def on_chat_model_start(
        self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], **kwargs
    ) -> None:
        print("Chat model started")

    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        print(f"Chat model ended, response: {response}")

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs
    ) -> None:
        print(f"Chain {serialized.get('name')} started")

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs) -> None:
        print(f"Chain ended, outputs: {outputs}")

callbacks = [LoggingHandler()]

openai_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, verbose=True)
qwen_llm = ChatOllama(model="qwen3:8b", max_tokens=256, verbose=True, callbacks=callbacks)
llm = openai_llm.with_fallbacks([qwen_llm])
chain = chat_prompt | llm

with patch("openai.resources.chat.completions.Completions.create", side_effect=Exception("OpenAI API error")):
    try:
        print(chain.invoke({"input_language": "中文", "output_language": "英文", "text": "今天天气很好。"}))
    except Exception as e:
        print("failed.")