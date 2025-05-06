import time
import asyncio
from langchain_deepseek import ChatDeepSeek

from langchain.schema import (
    AIMessage,
    BaseMessage,
    ChatMessage,
    HumanMessage,
    SystemMessage,
)
def generate_serially():
    llm = ChatDeepSeek(
        model="deepseek-chat",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # 其他参数...
    )
    for _ in range(10):
        resp = llm.generate([[HumanMessage(content = "Hello, how are you?")]])
        # 修正属性访问
        print(resp.generations[0][0].text)
    
async def async_generate(llm):
    resp = await llm.agenerate([[HumanMessage(content = "Hello, how are you?")]])
    # 修正属性访问
    print(resp.generations[0][0].text)

async def generate_concurrently():
    llm = ChatDeepSeek(
        model="deepseek-chat",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # 其他参数...
    )
    # 创建任务列表并发执行
    tasks = [async_generate(llm) for _ in range(10)]
    await asyncio.gather(*tasks)

# 测量并发执行时间
s = time.perf_counter()
asyncio.run(generate_concurrently())
elapsed = time.perf_counter() - s
print("\033[1m" + f"Concurrent executed in {elapsed:0.2f} seconds." + "\033[0m")

# 测量串行执行时间
s = time.perf_counter()
generate_serially()
elapsed = time.perf_counter() - s
print("\033[1m" + f"Serial executed in {elapsed:0.2f} seconds." + "\033[0m")

