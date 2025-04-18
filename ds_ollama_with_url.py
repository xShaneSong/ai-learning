import requests
import json

def chat_with_ollama(prompt, model="deepseek-r1:7b"):
    """
    与本地Ollama API进行交互的聊天函数
    
    参数:
    prompt -- 用户的输入内容 (str)
    model -- 要使用的模型名称 (默认: llama2)
    
    返回:
    tuple -- (状态码, 响应内容/错误信息)
    """
    url = "http://10.1.20.62:11434/api/chat"
    
    headers = {
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False  # 设置为True可以启用流式响应
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=300)
        response.raise_for_status()
        
        # 解析响应内容
        response_data = response.json()
        
        if 'message' in response_data and 'content' in response_data['message']:
            return (response.status_code, response_data['message']['content'])
            
        return (response.status_code, "Received unexpected response format")
        
    except requests.exceptions.RequestException as e:
        return (500, f"Request failed: {str(e)}")
    except json.JSONDecodeError:
        return (500, "Failed to parse JSON response")

# 使用示例
if __name__ == "__main__":
    status_code, response = chat_with_ollama(
        prompt="why is the sky blue?",
        model="deepseek-r1:7b"  # 请确保本地安装了对应的模型
    )
    
    if status_code == 200:
        print("Response:")
        print(response)
    else:
        print(f"Error ({status_code}): {response}")
