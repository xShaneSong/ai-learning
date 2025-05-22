import requests
import json
import os

API_ENDPOINT = "https://api.deepseek.com/chat/completions"
API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not API_KEY:
    raise ValueError("Please set the DEEPSEEK_API_KEY environment variable.")
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

class ContextManager:
    def __init__(self, max_turns=5):
        self.context = []
        self.max_turns = max_turns
        self.kv_cache = None  # 新增：用于缓存kv_cache

    def add_turn(self, user_input, model_response):
        self.context.append({"role": "user", "content": user_input})
        self.context.append({"role": "assistant", "content": model_response})
        if (len(self.context) > self.max_turns * 2):
            self.context = self.context[-self.max_turns * 2:]

    def get_context(self):
        # 返回消息列表
        return self.context.copy()

    def get_kv_cache(self):
        # 获取kv_cache
        return self.kv_cache

    def set_kv_cache(self, kv_cache):
        # 设置kv_cache
        self.kv_cache = kv_cache

def get_model_response(prompt, kv_cache=None):
    payload = {
        "model": "deepseek-chat",
        "messages": prompt,
        "temperature": 0.7,
        "max_tokens": 150,
        "top_p": 0.9,
    }
    if kv_cache is not None:
        payload["kv_cache"] = kv_cache  # 追加kv_cache到请求体

    response = requests.post(API_ENDPOINT, headers=HEADERS, json=payload)
    print(response.text)
    if response.status_code == 200:
        resp_json = response.json()
        # 提取kv_cache
        kv_cache = resp_json.get("kv_cache", None)
        content = resp_json.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        return content, kv_cache
    else:
        try:
            error_text = response.text
        except Exception:
            error_text = "<unable to decode response text>"
        return f"Error: {response.status_code} - {error_text}", None

def optimize_conversation():
    # 使用kv_cache缓存对话状态
    pass

conv_manager = ContextManager(max_turns=3)

user_input = [
    "你好，介绍一下人工智能？",
    "深度学习是人工智能的一部分吗？",
    "能否给我一个深度学习的例子？",
]

for input_text in user_input:
    context = conv_manager.get_context()
    context.append({"role": "user", "content": input_text})
    # 传递kv_cache
    model_response, kv_cache = get_model_response(context, conv_manager.get_kv_cache())
    conv_manager.add_turn(input_text, model_response)
    # 缓存最新的kv_cache
    conv_manager.set_kv_cache(kv_cache)
    print(f"User: {input_text}")
    print(f"Assistant: {model_response}")
    print("-" * 50)
    print(f"Context: {conv_manager.get_context()}")
    print("=" * 50)
