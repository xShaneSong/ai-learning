from openai import OpenAI
import json

def get_weather(location):
    if "dalian" in location:
        return json.dumps({"location": "dalian", "temperature": "15"})
        # return "15℃"
    elif "shenyang" in location:
        # return json.dumps({"location": "shenyang", "temperature": "10"})
        return "10℃"
    else:
        return json.dumps({"location": location, "temperature": "unknown"})

def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools
    )
    print(response)
    return response.choices[0].message

client = OpenAI(
    api_key="{api-key}",
    base_url="https://api.deepseek.com",
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather of an location, the user shoud supply a location first",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    }
                },
                "required": ["location"]
            },
        }
    },
]

messages = [{"role": "user", "content": "How's the weather in dalian?"}]
message = send_messages(messages)
print(f"User>\t {messages[0]['content']}")

tool = message.tool_calls[0]
messages.append(message)

function_args = json.loads(tool.function.arguments)
function_response = get_weather(
    location=function_args.get("location")
)
messages.append(
    {
        "tool_call_id": tool.id,
        "role": "tool",
        "content": function_response,
    }
)
# messages.append({"role": "tool", "tool_call_id": tool.id, "content": "24℃"})
message = send_messages(messages)
print(f"Model>\t {message.content}")