'''
This code is only for test DeepSeek api with sdk.
'''
from openai import OpenAI

client = OpenAI(
    api_key="sk-ec90e4d7506b49a990e08a1a89d50ee3",
    base_url="https://api.deepseek.com/v1",
)

response = client.chat.completions.create(
    # model="deepseek-chat",
    model="deepseek-reasoner",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "who are you?"},
    ],
    stream=False
)

# stream is False
print(response.choices[0].message.content)

# response = client.chat.completions.create(
#     model="deepseek-chat",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant"},
#         {"role": "user", "content": "how to use deepseek api"},
#     ],
#     stream=True
# )

# # stream is True 
# for chunk in response:
#     print(chunk)
#     print(chunk.choices[0].delta.content)
#     print("=====================")