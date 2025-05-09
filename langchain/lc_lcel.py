from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.chat_models import ChatOllama


llm = ChatOllama(model="qwen3:8b", max_tokens=256, temperature=0, verbose=True)

prompt = ChatPromptTemplate.from_template(
    """
    告诉我关于{input}的知名景点。
    """
)
output_parser = StrOutputParser()

chain = prompt | llm | output_parser
result = chain.invoke({"input": "大连"})
print(result)