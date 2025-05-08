from langchain.chains.conversation.base import ConversationChain
from langchain.memory.buffer import ConversationBufferMemory
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="qwen3:8b", temperature=0.1, max_tokens=512, verbose=True)

coversation = ConversationChain(
    llm=llm,
    memory=ConversationBufferMemory(),
    verbose=True,
)

coversation.run(
    "请告诉我3个知名的汽车品牌。"
)
coversation.run(
    "请再告诉我4个不同的知名的汽车品牌。"
)