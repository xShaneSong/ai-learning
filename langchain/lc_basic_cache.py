import time

start_time = time.perf_counter()

from langchain_ollama import OllamaLLM
from langchain.globals import set_llm_cache
from langchain_community.cache import InMemoryCache

from langchain_community.cache import SQLiteCache

set_llm_cache(SQLiteCache(database_path="cache.db"))
# set_llm_cache(InMemoryCache())

llm = OllamaLLM(model="qwen3:8b", max_tokens=256, verbose=True)
print(llm.invoke("What is the capital of France?"))
print(f"llm.invoke took {time.perf_counter() - start_time:.2f} seconds")
second_time = time.perf_counter()
print(llm.invoke("What is the capital of France?"))
print(f"llm.invoke took {time.perf_counter() - second_time:.2f} seconds")

