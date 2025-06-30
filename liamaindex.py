import time
import random
import asyncio
import threading
from collections import defaultdict
from functools import wraps
from typing import Dict,List, Any

# 缓存管理器类
class CacheManager:
    def __init__(self):
        self.cache = defaultdict(dict)  # 使用默认字典存储缓存

    def get(self, key: str) -> Any:
        return self.cache.get(key, None)  # 获取缓存内容

    def set(self, key: str, value: Any) -> None:
        self.cache[key] = value  # 设置缓存内容
        print(f"Cache set for key: {key}")

    def contains(self, key: str) -> bool:
        return key in self.cache  # 判断缓存是否存在

    def clear(self) -> None:
        with self.lock:
            self.cache.clear()  # 清空缓存

cache_manager = CacheManager()  # 实例化缓存管理器

# 缓存装饰器
def cache_result(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        query = args[0]
        if cache_manager.contains(query):
            print(f"Cache hit for query: {query}")
            return cache_manager.get(query)  # 命中缓存直接返回
        result = func(*args, **kwargs)
        cache_manager.set(query, result)  # 未命中则执行并缓存
        return result
    return wrapper

# 倒排索引类
class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(list)  # 存储倒排索引

    def build_index(self, documents: List[str]) -> None:
        for doc_id, content in enumerate(documents):
            for word in content.split():
                self.index[word].append(str(doc_id))  # 建立词到文档ID的映射

    def search(self, query: str) -> List[str]:
        return self.index.get(query, [])  # 查询关键词对应的文档ID列表

# 向量索引类
class VectorIndex:
    def __init__(self):
        self.vectors = defaultdict(dict)  # 存储文本及其向量和元数据

    def add_vector(self, text: str, vector: List[float], metadata: Dict) -> None:
        self.vectors[text] = {
            'vector': vector,
            'metadata': metadata
        }  # 添加向量及元数据

    def search_vector(self, query_vector: List[float], top_k: int = 2) -> List[Dict]:
        # 这里只是示例，返回固定结果
        return [{"text": "订单已发货", "metadata": {"status": "shipped"}}]

# 查询处理类
class QueryHandler:
    def __init__(self):
        self.inverted_index = InvertedIndex()  # 倒排索引实例
        self.vector_index = VectorIndex()      # 向量索引实例

    @cache_result
    def search(self, query: str) -> List[Any]:
        keyword_results = self.inverted_index.search(query)  # 关键词检索
        vector_results = self.vector_index.search_vector([random.random() for _ in range(10)], top_k=2)  # 向量检索
        return {"keyword_results": keyword_results, "vector_results": vector_results}
    
# 异步更新索引（使用线程）
def async_update_index(index: InvertedIndex, documents: List[str]) -> None:
    def update():
        print("Starting index update...")
        index.build_index(documents)
    thread = threading.Thread(target=update)
    thread.start()
    thread.join()

# 安全管理类
class SecurityManager:
    def __init__(self):
        self.authorized_users = {"admin": "password123"}  # 简单的用户认证信息

    def authenticate(self, username: str, password: str) -> bool:
        return self.authorized_users.get(username) == password  # 验证用户名和密码
    
# 知识库类
class KnowledgeBase:
    def __init__(self):
        self.query_handler = QueryHandler()      # 查询处理实例
        self.security_manager = SecurityManager()# 安全管理实例

    def query(self, user: str, password: str, query: str):
        if not self.security_manager.authenticate(user, password):
            raise PermissionError("Unauthorized Access")  # 未授权抛出异常
        return self.query_handler.search(query)           # 返回查询结果

# 日志装饰器，记录函数执行时间
@wraps
def log_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time for {func.__name__}: {end_time - start_time:.4f} seconds")
        return result
    return wrapper

# 主函数
@log_execution
def main():
    kb = KnowledgeBase()  # 创建知识库实例
    documents = ["订单已发货", "订单已取消", "订单已完成"]  # 示例文档
    async_update_index(kb.query_handler.inverted_index, documents)  # 异步构建索引
    
    try:
        result = kb.query("admin", "password123", "订单")  # 查询
        print("Query Result:", result)
    except PermissionError as e:
        print(e)

if __name__ == "__main__":
    main()