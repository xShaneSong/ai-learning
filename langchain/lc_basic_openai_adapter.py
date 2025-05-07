from langchain_community.adapters import openai as lc_openai

openai_api_key = "EMPTY"
openai_api_base = "http://localhost:11434/v1"

messages = [{"role": "user", "content": "你是谁?"}]

# lc_result = lc_openai.chat.completions.create(
#     messages=messages,
#     openai_api_key=openai_api_key,
#     openai_api_base=openai_api_base,
#     model="qwen3:8b",
#     temperature=0.7,
#     max_tokens=100,
#     stream=False
#     # top_p=1.0,
#     # frequency_penalty=0.0,
#     # presence_penalty=0.0,
#     # stop=None
# )

# print(lc_result)  # dict access

for c in lc_openai.chat.completions.create(
    messages=messages,
    openai_api_key=openai_api_key,
    openai_api_base=openai_api_base,
    model="qwen3:8b",
    temperature=0.7,
    max_tokens=100,
    stream=True
):
    print(c.choices[0].delta) 