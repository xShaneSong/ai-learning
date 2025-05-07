from langchain_core.output_parsers import XMLOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field, field_validator  # 从 pydantic 直接导入
from langchain_ollama import OllamaLLM
from langchain.output_parsers.json import SimpleJsonOutputParser

# 初始化模型
model = OllamaLLM(model="qwen3:8b", max_tokens=256, verbose=True)

# 定义数据结构
class Joke(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")

    # 添加自定义验证逻辑
    @field_validator("setup")
    def question_ends_with_question_mark(cls, field):
        if not field.endswith("?"):
            raise ValueError("Badly formed question!")
        return field

# 设置解析器并将格式说明注入到提示模板中
# parser = PydanticOutputParser(pydantic_object=Joke)
parser = XMLOutputParser()
parser.get_format_instructions()

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# 创建提示模板和模型的组合
prompt_and_model = prompt | model

# 调用模型并解析输出
output = prompt_and_model.invoke({"query": "Tell me a joke."})
parsed_output = parser.parse(output)

# 打印解析结果
print(parsed_output)