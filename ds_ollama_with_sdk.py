from ollama import chat
from ollama import ChatResponse

from ollama import Client
client = Client(
  host='http://localhost:11434',
#   headers={'x-some-header': 'some-value'}
)
# response = client.chat(
#     model='deepseek-r1:7b',
#     messages=[
#     {
#         'role': 'user',
#         'content': 'Why is the sky blue?',
#     }],
#     stream=False
#     )
# print(response.message.content)

# response: ChatResponse = chat(model='deepseek-r1:7b', messages=[
#   {
#     'role': 'user',
#     'content': 'Why is the sky blue?',
#   },
# ])
# print(response['message']['content'])
# or access fields directly from the response object

print('======================================\n')
response = client.chat(
    model='deepseek-r1:7b',
    messages=[
        {"role": "system", "content": "您是一个帮助用户了解鲜花信息的智能助手,并能够输出JSON格式的内容。"},
        {"role": "user", "content": "生日送什么花最好？"},
        {"role": "assistant", "content": "玫瑰是生日礼物的热门选择。"},
        {"role": "user", "content": "送货需要多长时间？"},
    ],
    stream=True
    )
for chunk in response:
  print(chunk['message']['content'], end='', flush=True)