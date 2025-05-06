from langchain_ollama import OllamaLLM
from langchain.callbacks.openai_info import get_openai_callback  # 更新导入路径

llm_qwen = OllamaLLM(
    model="qwen3:1.7b",
    max_tokens=256,
    verbose=True,
    streaming=True,
    # callbacks=[StreamingStdOutCallbackHandler()],
    temperature=0.1,
    n=2,
    best_of=2,
)

with get_openai_callback() as cb:
    result = llm_qwen.invoke("Write me a song about a cat.")
    print(cb)
    print("Total Tokens: ", cb.total_tokens)
    print("Total Cost: ", cb.total_cost)
    print("Prompt Tokens: ", cb.prompt_tokens)
    print("Completion Tokens: ", cb.completion_tokens)