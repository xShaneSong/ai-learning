from fastmcp import FastMCP
from fastapi import FastAPI
import uvicorn

# 初始化MCP服务实例
mcp_server = FastMCP("UserSystem")

# mcp_server = FastMCP(
#     name="UserSystem",
#     host="127.0.0.1",
#     port=9000, # Directly maps to ServerSettings
#     on_duplicate_tools="error" # Set duplicate handling
# )

# 获取 FastAPI 应用实例
# app = mcp_server.create_app()

# 添加根路径的处理逻辑
# @app.get("/")
# async def root():
#     return {"message": "MCP Server is running. Use the registered tools."}

# 注册工具函数
@mcp_server.tool()
async def add_user(name: str, age: int) -> dict:
    return {"status": "success", "user_id": 1001}

@mcp_server.tool()
async def query_user(user_id: int) -> dict:
    return {"user_id": user_id, "name": "John", "age": 28}

# 启动服务
if __name__ == "__main__":
    # mcp_server.run()
    mcp_server.run(transport="sse", host="127.0.0.1", port=9000, log_level="debug")
    # asyncio.run(
    #     mcp_server.run_sse_async(
    #         host="127.0.0.1", 
    #         port=8888, 
    #         log_level="debug"
    #     )
    # )
    # uvicorn.run(app, host="127.0.0.1", port=9000, log_level="debug")
