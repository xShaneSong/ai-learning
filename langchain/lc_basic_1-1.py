import os
# os.environ['NO_PROXY'] = 'localhost,127.0.0.1,10.0.0.0/8,::1'

from langchain_ollama import OllamaLLM

llm_qwen = OllamaLLM(model="qwen3:8b", max_tokens=256, verbose=True)
print(llm_qwen.invoke("What is the capital of France?"))
