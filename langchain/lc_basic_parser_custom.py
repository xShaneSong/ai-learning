from typing import Iterable
from langchain_ollama import OllamaLLM
from langchain_core.messages import AIMessage, AIMessageChunk
from langchain_core.runnables import RunnableGenerator

# 初始化 OllamaLLM 模型
llm = OllamaLLM(model="qwen3:8b", max_tokens=256, verbose=True)

# 定义解析函数，将 AI 消息的大小写反转
def parse(ai_message: AIMessage) -> str:
    """解析 AI 消息，将消息中的字符大小写反转。"""
    return ai_message.swapcase()

# 定义流式解析函数，将每个消息块的大小写反转
def streaming_parse(chunks: Iterable[AIMessageChunk]) -> Iterable[str]:
    """流式解析 AI 消息块，将每个块的字符大小写反转。"""
    for chunk in chunks:
        yield chunk.swapcase()

# 将流式解析函数封装为 RunnableGenerator
streaming_parse = RunnableGenerator(streaming_parse)

# 链式调用示例：将模型和流式解析器组合
chain = llm | streaming_parse 
for chunk in chain.stream("What is the capital of France?"):
    print(chunk, end="", flush=True)

############## 自定义输出解析器 ###############

print("################# 自定义输出解析器 #################")
from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import BaseOutputParser

# 定义自定义布尔解析器
class BooleanOutputParser(BaseOutputParser[bool]):
    """自定义布尔解析器，用于解析模型输出为布尔值。"""

    true_val: str = "YES"  # 定义表示 True 的值
    false_val: str = "NO"  # 定义表示 False 的值

    # 接收模型输出的字符串并进行解析
    def parse(self, text: str) -> bool:
        """解析模型输出，将其转换为布尔值。"""
        cleaned_text = text.strip().upper()  # 清理文本并转换为大写
        if cleaned_text not in (self.true_val.upper(), self.false_val.upper()):
            # 如果输出不在预期值范围内，抛出异常
            raise OutputParserException(
                f"BooleanOutputParser 期望输出值为 "
                f"{self.true_val} 或 {self.false_val}（不区分大小写）。"
                f"接收到的值为 {cleaned_text}。"
            )
        return cleaned_text == self.true_val.upper()  # 返回布尔值

    # 标识解析器名称
    @property
    def _type(self) -> str:
        return "boolean_output_parser"

# # 初始化布尔解析器
# parser = BooleanOutputParser()

# # 将模型和布尔解析器组合成链
# chain = llm | parser
# print(chain.invoke("请回复 YES或NO: 你喜欢Python吗？"))

############### 自定义输出解析器2 ###############

print("################# 自定义输出解析器2 #################")

from typing import List
from langchain_core.exceptions import OutputParserException
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import BaseGenerationOutputParser
from langchain_core.outputs import ChatGeneration, Generation

# 定义自定义字符串大小写反转解析器
class StrInvertCase(BaseGenerationOutputParser[str]):
    """A parser to invert the case of characters in the model's output."""

    def parse_result(self, result: List[Generation], *, partial: bool = False) -> str:
        """Parse the model's output and invert the case of the content.

        Args:
            result: A list of generation results.
            partial: Whether partial results are allowed (for streaming).

        Returns:
            A string with inverted case.
        """
        if len(result) != 1:
            raise NotImplementedError("This parser only supports a single generation result.")

        generation = result[0]

        # Handle both ChatGeneration and Generation types
        if isinstance(generation, ChatGeneration):
            content = generation.message.content
        elif isinstance(generation, Generation):
            content = generation.text
        else:
            raise OutputParserException("Unsupported generation type for this parser.")

        # Return the content with inverted case
        return content.swapcase()

# 初始化字符串大小写反转解析器
chain2 = llm | StrInvertCase()
print(chain2.invoke("Tell me a short sentence about yourself"))