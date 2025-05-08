from langchain_ollama import OllamaEmbeddings

# 嵌入文档
embeddings_model = OllamaEmbeddings(model="nomic-embed-text")
embeddings = embeddings_model.embed_documents(
    [
        "嗨",
        "你好",
        "你叫什么名字",
    ]
)

len(embeddings)
len(embeddings[0])
print(len(embeddings), len(embeddings[0]))
# print(embeddings[:5])

# 嵌入查询
embedded_query = embeddings_model.embed_query("在这个对话中提到了什么名字？")
print(embedded_query[:5])

# 缓存向量
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import (
    InMemoryByteStore,
    LocalFileStore,
)

# store = InMemoryByteStore()
store = LocalFileStore("./test_cache")
underlying_embeddings = OllamaEmbeddings(model="nomic-embed-text")
cache_backed_embeddings = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings, store, namespace=underlying_embeddings.model
)
embeddings = cache_backed_embeddings.embed_documents(
    [
        "嗨",
        "你好",
        "你叫什么名字",
    ]
)

len(embeddings)
len(embeddings[0])
print(len(embeddings), len(embeddings[0]))

# Fake embeddings
from langchain_core.embeddings.fake import FakeEmbeddings
fake_embeddings = FakeEmbeddings(size=100)
query_result = fake_embeddings.embed_query("hello world")
print(query_result)
doc_result = fake_embeddings.embed_documents(["hello world"])
print(doc_result)