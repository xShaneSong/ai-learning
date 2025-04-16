from langchain_ollama import OllamaLLM
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

# 创建Ollama实例
llm = OllamaLLM(
    model="deepseek-r1:7b",  # 替换为实际模型名称
    base_url='http://localhost:11434',  # 本地Ollama服务地址
    # temperature=0.7,       # 控制生成随机性（0-1）
    # num_ctx=2048        # 上下文长度
)

template = """Question:{question}
Answer: Let's think step by step."""

# Ensure input_variables matches the variable in the template
prompt = PromptTemplate(template=template, input_variables=["question"])
# Define the question
question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"

#llm_chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
# print(llm_chain.run(question))

chain = prompt | llm
print(chain.invoke(question))