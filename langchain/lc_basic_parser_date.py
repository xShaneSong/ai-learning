from langchain.output_parsers.datetime import DatetimeOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama.chat_models import ChatOllama
# from langchain.chains import LLMChain

# 初始化输出解析器
output_parser = DatetimeOutputParser()
format_instructions = output_parser.get_format_instructions()

# 定义提示模板
template = """回答用户以下问题：
{question}
{format_instructions}"""
prompt = PromptTemplate(
    input_variables=["question"],
    template=template,
    partial_variables={"format_instructions": format_instructions},
)

# 初始化模型
model = ChatOllama(model="qwen3:8b", max_tokens=256, verbose=True)

# 创建 LLMChain
chain = prompt | model | output_parser
# chain = LLMChain(prompt=prompt, llm=model, output_parser=output_parser)

# 调用链并处理返回值
response = chain.invoke({"question": "中国的国庆节是哪一天？"})

# 提取并打印结果
if hasattr(response, "content"):
    print(response.content)  # 提取 AIMessage 的内容
else:
    print(response)  # 如果是字符串，直接打印