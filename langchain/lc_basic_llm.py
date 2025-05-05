from langchain_ollama import OllamaLLM

# llm_qwen3 = OllamaLLM(model = "qwen3:1.7b")
llm_ds15 = OllamaLLM(model = "deepseek-r1:1.5b")
llm_ds8 = OllamaLLM(model = "deepseek-r1:8b")
print(llm_ds15.invoke("What is the capital of France?"))