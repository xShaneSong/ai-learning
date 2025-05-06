from langchain_ollama import OllamaLLM

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

llm_qwen = OllamaLLM(model="qwen3:1.7b", max_tokens=256,
                     verbose=True,
                     streaming =True,
                     callbacks=[StreamingStdOutCallbackHandler()],
                     temperature=0.1)
print(llm_qwen.invoke("Write me a song about a cat."))