from typing import List

from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import BaseOutputParser
from langserve import add_routes
from langserve import RemoteRunnable

# define chain
class CommaSeparatedListOutputParser(BaseOutputParser):
    def parse(self, output: str) -> List[str]:
        return output.split(", ")
    
template = """用户会传入一个类型，你唯一拥有生成该类型下的5个对象，并以逗号分隔的能力。请生成这5个对象。
只返回以逗号分隔的5个对象，不要返回其他内容。"""
human_template = "{text}"

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template)
])

first_chain = chat_prompt | ChatOpenAI() | CommaSeparatedListOutputParser()

# create app
app = FastAPI(
    title="LangChain",
    description="A language chain service",
    version="0.1.0"
)

# add routes
add_routes(app, first_chain, path="/first_app")

# run app
if __name__ == "__main__":
    # import uvicorn
    # uvicorn.run(app, host="localhost", port=8000)
    remote_chain = RemoteRunnable(app, "http://localhost:8000/first_app")

    print(remote_chain.invoke({"text": "person"}))