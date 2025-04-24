from fastmcp import FastMCP, Client

mcp = FastMCP("My MCP Server")

@mcp.tool()
def greet(name: str) -> str:
    print("Hello world")
    return f"Hello, world--{name}!"

if __name__ == "__main__":
    # mcp.run()
    mcp.run(transport="sse", host="127.0.0.1", port=9000)