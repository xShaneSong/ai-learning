from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.llms import DeepSeek
# from openai import OpenAI
# from langchain_core.runnables import RunnableLLM
from langchain_openai import ChatOpenAI

import os

def load_and_process_pdfs(pdf_dir, chunk_size=500, chunk_overlap=50):
    """加载目录下所有PDF文档并进行预处理:ml-citation{ref="2,7" data="citationList"}"""
    loader = DirectoryLoader(
        path=pdf_dir,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True
    )
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(documents)

def create_vector_store(splits, embedding_model="BAAI/bge-small-zh-v1.5"):
    """创建向量存储:ml-citation{ref="1,5" data="citationList"}"""
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
    return FAISS.from_documents(splits, embeddings)

def setup_rag_chain(vectorstore, temperature=0.1):
    """配置RAG链式流程:ml-citation{ref="5,6" data="citationList"}"""
    # 初始化DeepSeek模型
    # llm = DeepSeek(
    #     api_key="sk-ec90e4d7506b49a990e08a1a89d50ee3",
    #     base_url="https://api.deepseek.com",
    #     model="deepseek-chat",
    #     temperature=temperature
    # )

    llm = ChatOpenAI(
        model="deepseek-chat",  # 指定 DeepSeek 支持的模型
        temperature=0.1,
        openai_api_key="{api-key}",  # 替换为你的 DeepSeek API 密钥
        openai_api_base="https://api.deepseek.com/v1"  # DeepSeek 的 API 基础地址
    )
    
    # Wrap the LLM in RunnableLLM
    # runnable_llm = RunnableLLM(llm)
    
    # 构建可并行处理组件
    retriever = vectorstore.as_retriever()
    setup = RunnableParallel(
        context=retriever,
        question=RunnablePassthrough()
    )
    
    # 定义提示模板
    prompt = ChatPromptTemplate.from_template(
        """基于以下上下文信息回答问题。保持回答专业准确。
        
        上下文:
        {context}
        
        问题: {question}
        
        回答:"""
    )
    
    return setup | prompt | llm

if __name__ == "__main__":
    # 配置参数
    PDF_DIR = "./data"  # 存放多个PDF的目录
    INDEX_PATH = "./storage/lc"  # 向量存储路径
    EMBEDDING_MODEL = "BAAI/bge-small-zh-v1.5"  # 嵌入模型名称
    
    # 1. 加载和处理文档
    if not os.path.exists(INDEX_PATH):
        splits = load_and_process_pdfs(PDF_DIR)
        vectorstore = create_vector_store(splits, embedding_model=EMBEDDING_MODEL)
        vectorstore.save_local(INDEX_PATH)
    else:
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        vectorstore = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    
    # 2. 创建RAG链
    rag_chain = setup_rag_chain(vectorstore)
    
    # 3. 交互式问答
    messages = [
        "比较一下两个公司的销售额。请使用中文回答。",
        "请预测未来两个公司的销售额趋势。",
    ]
    for message in messages:
        print(rag_chain.invoke(message).content)