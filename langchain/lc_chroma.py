from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters.character import CharacterTextSplitter
from langchain_chroma.vectorstores import Chroma
from langchain_community.document_loaders.text import TextLoader

loader = TextLoader("../README.md", encoding="utf-8")
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embedding_function = OllamaEmbeddings(model="nomic-embed-text")
db = Chroma.from_documents(docs, embedding_function)

query = ("马斯克认为AI将对人类文明产生什么影响？")
docs = db.similarity_search(query)
print(docs[0].page_content)

db2 = Chroma.from_documents(docs, embedding_function, persist_directory="./chroma_db")
docs = db2.similarity_search(query)
print(docs[0].page_content)

db3 = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)
docs = db3.similarity_search(query)
print(docs[0].page_content)

# chroma client
import chromadb

persistent_client = chromadb.PersistentClient()
collection = persistent_client.get_or_create_collection(
    name="collection_name",
)

# insert
collection.add(ids=["1", "2", "3"], documents=["doc1", "doc2", "doc3"])
langchain_chroma = Chroma(
    client = persistent_client,
    collection_name="collection_name",
    embedding_function=embedding_function,
)
print("There are", langchain_chroma._collection.count(), "documents in the collection.")

# update
docs[0].metadata = {
    "source": "README.md",
    "new_value": "new_value"
}

ids = [str(i) for i in range(1, len(docs) + 1)]
db.update_document(ids[0], docs[0])
print(db._collection.count())
print(db._collection.get(ids = [ids[0]]))

db._collection.delete(ids = [ids[-1]])
print(db._collection.count())
docs = db.similarity_search(query)
print(docs[0].page_content)
