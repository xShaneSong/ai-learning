from langchain_ollama import OllamaLLM
import os
from langchain_community.llms.loading import load_llm
from langchain_deepseek import ChatDeepSeek
from langchain_core.load import dumpd, dumps, load, loads
import json

if __name__ == "__main__":
    if os.sys.argv[1] == "save":
        # llm = OllamaLLM(model="qwen3:8b", max_tokens=256, verbose=True)
        llm = ChatDeepSeek(
            model="deepseek-chat",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            # 其他参数...
        )
        # llm.save("qwen3_8b_model.json")
        # llm.save("qwen3_8b_model.yaml")
        string_representation = dumps(llm, pretty=True)
        print(string_representation[:500])

        with open("dump_llm.json", "w") as fp:
            json.dump(string_representation, fp)
    elif os.sys.argv[1] == "load":

        # ValueError: Loading ollama-llm LLM not supported
        # llm = load_llm("qwen3_8b_model.yaml")
        # print(llm.invoke("What is the capital of France?"))

        with open("dump_llm.json", "r") as fp:
            llm = loads(json.load(fp))
            print(llm.invoke("What is the capital of France?"))