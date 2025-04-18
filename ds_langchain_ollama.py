# 安装必要库（如果尚未安装）
# pip install langchain langchain-community ollama

from langchain_ollama import OllamaLLM

# model = OllamaLLM(model="llama3")

# 1. 首先确保Ollama服务正在运行（终端执行）：
# ollama serve

# 2. 确认DeepSeek模型已下载/创建（例如执行）：
# ollama pull deepseek-llm:latest  # 如果官方提供
# 或使用自定义Modelfile创建

# 创建Ollama实例
llm = OllamaLLM(
    model="deepseek-r1:7b",  # 替换为实际模型名称
    base_url='http://10.1.20.62:11434',  # 本地Ollama服务地址
    #temperature=0.7,       # 控制生成随机性（0-1）
    # num_ctx=2048        # 上下文长度
)

# 调用模型生成响应
response = llm.invoke("who are you")
print("模型回复：", response)

# 使用流式响应（适合长文本）
for chunk in llm.stream("如何制作一杯好的绿茶？步骤："):
    print(chunk, end="", flush=True)
