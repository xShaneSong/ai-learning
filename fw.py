import asyncio
import time
import random
from typing import List, Dict, Any, Callable
from functools import wraps

class FakeLLM:
    def __init__(self, temperature: float = 0.5):
        self.temperature = temperature
    
    def __call__(self, prompt: str) -> str:
        responses = {
            "Hello, Alice!": "Hello, Bob!Nice to meet you!",
            "Fetching data for Machine Learning.": "Here is the latest data on Machine Learning.",
        }
        return responses.get(prompt, "I have no idea what you are asking.")

class LangChainAgent:
    def __init__(self, llm: FakeLLM):
        self.context = {}
        self.tasks = []
        self.llm = llm

    def add_task(self, task: Callable, name: str = None):
        task_name = name if name else function.__class__.__name__
        print(f"Adding task: {task_name}")
        self.tasks.append((task, task_name))

    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        data = input_data
        for task, name in self.tasks:
            print(f"Running task: {name}")
            result = await task(data)
        return result
    
class TemplateTask:
    def __init__(self, template: str, llm: FakeLLM):
        self.template = template
        self.llm = llm
    
    async def __call__(self, data: Dict[str, Any]) -> str:
        await asyncio.sleep(random.uniform(0.1, 0.5))  # Simulate network delay
        input_value = data.get('name') or data.get('query', 'unknown')
        prompt = self.template.format(name_or_query=input_value)
        response = self.llm(prompt)
        print(f"Task completed: {response}")
        return {"response": response}
        
class RouteChain:
    def __init__(self, routes: Dict[str, Callable]):
        self.routes = routes

    async def execute(self, condition: str, input_data: Dict[str, Any]):
        if condition in self.routes:
            print(f"Routing to {condition}...")
            await self.routes[condition](input_data)
        else:
            print(f"No route found for condition: {condition}")
        
class PerfomanceMonitor:
    def __init__(self):
        self.execution_times = []

    def log_time(self, func: Callable, task_name: str = None):
        task_name = task_name if task_name else func.__class__.__name__
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            result = await func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            self.execution_times.append(elapsed_time)
            print(f"Task {task_name} executed in {elapsed_time:.2f} seconds")
            return result
        return wrapper
    
    def report(self):
        total_time = sum(self.execution_times)
        print(f"Total execution time for all tasks: {total_time:.2f} seconds")
        print(f"Average execution time: {total_time / len(self.execution_times):.2f} seconds" if self.execution_times else "No tasks executed.")

llm = FakeLLM(temperature=0.5)
monitor = PerfomanceMonitor()
agent = LangChainAgent(llm)

greet_task = TemplateTask("Hello, {name_or_query}!", llm)
query_task = TemplateTask("Fetching data for {name_or_query}.", llm)
agent.add_task(monitor.log_time(greet_task, "Greeting Task"))
agent.add_task(monitor.log_time(query_task, "Query Task"))

router = RouteChain(routes={
    "greet": lambda data: agent.run(data),
    "query": lambda data: agent.run(data),
})

@monitor.log_time
async def main():
    print("Starting the LangChain Agent...")
    await router.execute("greet", {"name": "Alice"})
    await router.execute("query", {"query": "Machine Learning"})
    monitor.report()

if __name__ == "__main__":
    asyncio.run(main())
