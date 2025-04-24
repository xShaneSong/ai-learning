# import requests

# class MCPClient:
#     def __init__(self, base_url="http://127.0.0.1:9000/sse"):
#         self.base_url = base_url
        
#     def execute_tool(self, tool_name: str, params: dict):
#         # Call the specific endpoint for the tool
#         endpoint = f"{self.base_url}/{tool_name}"
#         response = requests.post(endpoint, json=params)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             return {"error": f"Failed to call tool {tool_name}. HTTP {response.status_code}"}

# # 使用示例
# if __name__ == "__main__":
#     client = MCPClient()
#     print(client.execute_tool("add_user", {"name": "Alice", "age": 25}))  # 添加用户
#     print(client.execute_tool("query_user", {"user_id": 1001}))  # 查询用户

import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    # 创建一个 SSE 客户端会话
    async with sse_client("http://127.0.0.1:9000/sse") as streams:
        # 使用 SSE 流初始化 ClientSession
        async with ClientSession(*streams) as session:
            # 初始化会话
            await session.initialize()
            
            # 获取可用的工具列表
            tools = await session.list_tools()
            print("Available tools:", tools)

            # 调用 add_user 工具
            add_user_result = await session.call_tool("add_user", {"name": "Alice", "age": 25})
            print("Add User Result:", add_user_result)

            # 调用 query_user 工具
            query_user_result = await session.call_tool("query_user", {"user_id": 1001})
            print("Query User Result:", query_user_result)

if __name__ == "__main__":
    asyncio.run(main())


# from fastmcp import Client
# import asyncio

# async def call_tools():
#     # 初始化 MCP 客户端，连接到运行的 MCP 服务
#     client = Client("http://localhost:9000/tool/")  # MCP 服务的 URL

#     async with client:
#         # 调用 add_user 工具
#         add_user_result = await client.call_tool("add_user", {"name": "Alice", "age": 25})
#         print("Add User Result:", add_user_result)

#         # 调用 query_user 工具
#         query_user_result = await client.call_tool("query_user", {"user_id": 1001})
#         print("Query User Result:", query_user_result)

# # 异步运行客户端
# if __name__ == "__main__":
#     asyncio.run(call_tools())
