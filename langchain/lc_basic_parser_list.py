from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama.chat_models import ChatOllama

# 初始化输出解析器
output_parser = CommaSeparatedListOutputParser()
format_instructions = output_parser.get_format_instructions()

# 定义提示模板
# prompt = PromptTemplate(
#     input_variables=["input_language", "output_language", "text"],
#     template="你是一个翻译助理，请将用户输入的内容由{input_language}翻译为{output_language}。{format_instructions}",
#     partial_variables={"format_instructions": format_instructions},
# )
prompt = PromptTemplate(
    template = "列出5个知名的{subject}.\n{format_instructions}",
    input_variables=["subject"],
    partial_variables={"format_instructions": format_instructions},
)

# 初始化模型
model = ChatOllama(model="qwen3:8b", max_tokens=256, verbose=True)

# 格式化输入
_input = prompt.format(subject="汽车品牌名称")

# 调用模型
response = model.invoke(_input)

# 提取模型输出为字符串
if hasattr(response, "content"):
    response_text = response.content  # 提取 AIMessage 的内容
else:
    response_text = str(response)  # 如果是字符串，直接使用

# 解析输出
output = output_parser.parse(response_text)
print(output)