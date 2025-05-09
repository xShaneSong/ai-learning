from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_ollama.chat_models import ChatOllama

# Define the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "你是一个AI助手。"
        ),
        # MessagesPlaceholder(variable_name="history"),  # Placeholder for chat history
        # MessagesPlaceholder("history"),  # Placeholder for chat history
        ("placeholder", "{chat_history}"),
        HumanMessagePromptTemplate.from_template("{input}"),  # Placeholder for user input
    ]
)

# Define the LLM
llm = ChatOllama(model="qwen3:8b", max_tokens=256, temperature=0, verbose=True)

# Combine the prompt and LLM into a runnable
runnable = prompt | llm

# Store for session histories
store = {}

# def get_session_history(session_id: str) -> BaseChatMessageHistory:
def get_session_history(user_id: str, conversation_id: str) -> BaseChatMessageHistory:
    """
    获取会话历史记录
    """
    # if session_id not in store:
        # store[session_id] = ChatMessageHistory()
    # return store[session_id]
    if (user_id, conversation_id) not in store:
        store[(user_id, conversation_id)] = ChatMessageHistory()
    return store[(user_id, conversation_id)]

# Wrap the runnable with message history management
with_message_history = RunnableWithMessageHistory(
    runnable=runnable,
    get_session_history=get_session_history,
    input_message_key="input",  # Key for user input
    output_message_key="history",  # Key for chat history
    history_factory_config=[
        ConfigurableFieldSpec(
            id = "user_id",
            annotation=str,
            name="User ID",
            description="Unique identifier for the user",
            default="",
            is_shared=True,
        ),
        ConfigurableFieldSpec(
            id = "conversation_id",
            annotation=str,
            name="Conversation ID",
            description="Unique identifier for the conversation",
            default="",
            is_shared=True,
        ),
    ]
)

# Invoke the runnable with session management
response_1 = with_message_history.invoke(
    {
        "input": "你能告诉我关于大连的知名景点吗？",
    },
    config={
        "configurable": {
            # "session_id": "session_0001"  # Specify session ID
            "user_id": "user_001",  # Specify user ID
            "conversation_id": "conv_001"  # Specify conversation ID
        }
    }
)
print("Response 1:", response_1)

response_2 = with_message_history.invoke(
    {
        "input": "你能给我详细介绍一下这些景点吗？",
    },
    config={
        "configurable": {
            # "session_id": "session_0001"  # Use the same session ID to maintain history
            "user_id": "user_001",  # Specify user ID
            "conversation_id": "conv_001"  # Specify conversation ID
        }
    }
)
print("Response 2:", response_2)

# from langchain_core.runnables import ConfigurableFieldSpec
