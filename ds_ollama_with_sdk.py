from ollama import chat
from ollama import ChatResponse

from ollama import Client
client = Client(
  host='http://localhost:11434',
#   headers={'x-some-header': 'some-value'}
)
response = client.chat(
    model='deepseek-r1:7b',
    messages=[
    {
        'role': 'user',
        'content': 'Why is the sky blue?',
    }],
    stream=False
    )
print(response.message.content)

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
    {
        'role': 'user',
        'content': 'Why is the sky blue?',
    }],
    stream=True
    )
for chunk in response:
  print(chunk['message']['content'], end='', flush=True)