from langchain_ollama.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableParallel

llm = ChatOllama(model="qwen3:8b", max_tokens=256, temperature=0, verbose=True)
prompt = ChatPromptTemplate.from_template(
    """
    告诉我关于{input}的知名景点。
    """
)
chain = prompt | llm | StrOutputParser()

analysis_prompt = ChatPromptTemplate.from_template(
    """
    请推荐一个性价比高的旅游目的地。
    {input2}
    """
)

composed_chain = {"input2" :chain} | analysis_prompt | llm | StrOutputParser()
# result = composed_chain.invoke({"input": "大连"})
# print(result)

composed_chain_with_lambda = (
    chain
    | (lambda input2: {"input2": input2})
    | analysis_prompt
    | llm
    | StrOutputParser(keep_input=True, keep_output=True)
)
# composed_chain_with_lambda.invoke({"input": "大连"})

composed_chain_with_lambda.get_graph().print_ascii()

print(composed_chain_with_lambda.get_prompts())

# result = composed_chain_with_lambda.invoke({"input": "大连"})
# print(result)

composed_chain_with_pipe = (
    RunnableParallel({
        "input2": chain,
    }).pipe(analysis_prompt)
    .pipe(llm)
    .pipe(StrOutputParser(keep_input=True, keep_output=True))
)
result = composed_chain_with_lambda.invoke({"input": "大连"})
print(result)
