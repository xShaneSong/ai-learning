import requests
import json
import time

def stream_ollama_response(prompt, model="deepseek-r1:7b", timeout=30):
    """
    处理Ollama流式响应的生成器函数
    
    参数:
    prompt -- 用户的输入内容 (str)
    model -- 要使用的模型名称 (默认: llama2)
    timeout -- 请求超时时间（秒）
    
    生成:
    tuple -- (状态码, 响应内容) 或错误信息
    """
    url = "http://10.1.20.62:11434/api/chat"
    
    headers = {
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True  # 启用流式响应
    }
    
    full_response = []
    
    try:
        with requests.post(url, 
                         headers=headers, 
                         json=payload, 
                         timeout=timeout,
                         stream=True) as response:
            
            response.raise_for_status()
            
            # 实时处理每个数据块
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line.decode('utf-8'))
                        if 'message' in chunk and 'content' in chunk['message']:
                            content = chunk['message']['content']
                            full_response.append(content)
                            yield (200, content)  # 实时生成每个片段
                            
                    except json.JSONDecodeError:
                        yield (500, "Invalid JSON chunk received")
                        break
                        
            # 返回完整响应
            yield (200, "".join(full_response))
            
    except requests.exceptions.RequestException as e:
        yield (500, f"Request failed: {str(e)}")
    except KeyboardInterrupt:
        yield (499, "User interrupted the request")
    except Exception as e:
        yield (500, f"Unexpected error: {str(e)}")

# 使用示例
if __name__ == "__main__":
    try:
        # 初始化生成器
        response_stream = stream_ollama_response(
            prompt="why is the sky blue? Please answer in Chinese.",
            # prompt="为什么天空是蓝色的？",
            model="deepseek-r1:7b",
            timeout=60
        )
        
        # 实时处理响应
        for status, chunk in response_stream:
            if status == 200:
                print(chunk, end="", flush=True)  # 逐字实时输出
            else:
                print(f"\n[error] {chunk}")
                break
                
    except KeyboardInterrupt:
        print("\n\nUser interrupt")
        
    print("\n\nFinlish.")
