from langchain_ollama import OllamaLLM
import os

if __name__ == "__main__":
    if os.sys.argv[1] == "save":
        llm = OllamaLLM(model="qwen3:8b", max_tokens=256, verbose=True)
        llm.save("qwen3_8b_model.json")
        llm.save("qwen3_8b_model.yaml")
    elif os.sys.argv[1] == "load":
        llm = OllamaLLM.load("qwen3_8b_model.json")
        print(llm.invoke("What is the capital of France?"))