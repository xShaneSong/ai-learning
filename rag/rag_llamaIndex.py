from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.llms import ChatMessage
from llama_index.llms.deepseek import DeepSeek
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# 配置大模型
# from llama_index.llms.openai import OpenAI
# llm = OpenAI(model="gpt-3.5-turbo-0613")
Settings.llm = DeepSeek(
    api_key="{api-key}",  # 替换为实际API Key
    model="deepseek-chat",
    temperature=0.1,
    max_tokens=2048
)

# 配置嵌入模型（HuggingFace模型）
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-zh-v1.5"  # 推荐的中文嵌入模型
)

from llama_index.core import SimpleDirectoryReader

# 加载数据
A_docs = SimpleDirectoryReader(
    input_files = ['./data/A-data.pdf']
).load_data()

B_docs = SimpleDirectoryReader(
    input_files = ['./data/B-data.pdf']
).load_data()

# 从文档中创建索引
from llama_index.core import VectorStoreIndex
A_index = VectorStoreIndex(A_docs)
B_index = VectorStoreIndex(B_docs)

# 持久化索引（保存到本地）
from llama_index.core import StorageContext
A_index.storage_context.persist(
    persist_dir = './storage/A'
)
B_index.storage_context.persist(
    persist_dir = './storage/B'
)

# 从本地读取索引
from llama_index.core import load_index_from_storage
try:
    storage_context = StorageContext.from_defaults(
        persist_dir="./storage/A"
    )
    A_index = load_index_from_storage(storage_context)

    storage_context = StorageContext.from_defaults(
        persist_dir="./storage/B"
    )
    B_index = load_index_from_storage(storage_context)

    index_loaded = True
except:
    index_loaded = False

# 创建查询引擎
A_engine = A_index.as_query_engine(similarity_top_k=3)
B_engine = B_index.as_query_engine(similarity_top_k=3)

# 配置查询工具
from llama_index.core.tools import QueryEngineTool
from llama_index.core.tools import ToolMetadata
query_engine_tools = [
    QueryEngineTool(
        query_engine=A_engine,
        metadata=ToolMetadata(
            name="A_Finance",
            description=(
                "用于提供A公司的财务信息 "
            ),
        ),
    ),
    QueryEngineTool(
        query_engine=B_engine,
        metadata=ToolMetadata(
            name="B_Finance",
            description=(
                "用于提供B公司的财务信息 "
            ),
        ),
    ),
]



# 创建ReAct Agent
from llama_index.core.agent import ReActAgent
agent = ReActAgent.from_tools(query_engine_tools, llm=Settings.llm, verbose=True)


# # 让Agent完成任务
# agent.chat("比较一下两个公司的销售额。请使用中文回答。")

# 多轮对话示例
messages = [
    "比较一下两个公司的销售额。请使用中文回答。",
    "请预测未来两个公司的销售额趋势。",
]

# for response in agent.stream_chat(messages):
#     print(f"Agent响应：{response}")
for message in messages:
    agent.chat(message)
