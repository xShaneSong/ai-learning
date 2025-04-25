
# using mcp_client to assess mcp server
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


# use fastmcp client to assess mcp server
from fastmcp import Client, FastMCP
import asyncio

server_instance = FastMCP("UserSystem", port=9000)

async def call_tools():
    # 初始化 MCP 客户端，连接到运行的 MCP 服务
    client = Client("http://localhost:9000/sse")
    async with client:
        # 获取可用的工具列表
        tools = await client.list_tools()
        print("Available tools:", tools)

        # 调用 add_user 工具
        add_user_result = await client.call_tool("add_user", {"name": "Alice", "age": 25})
        print("Add User Result:", add_user_result)

        # 调用 query_user 工具
        query_user_result = await client.call_tool("query_user", {"user_id": 1001})
        print("Query User Result:", query_user_result)

# 异步运行客户端
if __name__ == "__main__":
    asyncio.run(call_tools())
