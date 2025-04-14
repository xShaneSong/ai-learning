import requests
import json

# DeepSeek API的URL
url = "https://api.deepseek.com/chat/completions"
api_key="{api-key}"

# 请求的headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# 请求的data
# data = {
#     "model": "deepseek-chat",
#     "messages": [
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "who are you?"}
#     ],
#     "stream": False
# }

# # 发送POST请求
# response = requests.post(url, headers=headers, data=json.dumps(data))

# # 输出响应内容
# print(response.json())

data = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "who are you?"}
    ],
    "stream": True
}

# 发送流式请求
with requests.post(url, headers=headers, json=data, stream=True) as response:  # 客户端启用流式处理‌:ml-citation{ref="4,8" data="citationList"}
    if response.status_code == 200:
        # 逐行读取流式响应
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if "[DONE]" in decoded_line:
                    break
                # 处理SSE格式数据（data: {...}）
                if decoded_line.startswith('data:'):
                    json_data = json.loads(decoded_line[5:].strip())
                    # choices = json_data['choices']
                    # delta = choices[0]['delta']
                    content = json_data['choices'][0]['delta']['content'] 
                    print(content)
                    # content = json_data['choices']['delta']['content']
                    # print(repr(content))  # 输出: ''
    else:
        print(f"请求失败，状态码：{response.status_code}")
