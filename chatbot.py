from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="./db",
    embedding_function=embeddings
)

retriever = db.as_retriever()

llm = Ollama(
    model="llama3",
    base_url="http://localhost:11434"
)

# Initialize QA chain for API use
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever
)

# Uncomment the following lines if you want to run the CLI version separately
# while True:
#     query = input("Ask: ")
#     response = qa.run(query)
#     print("Bot:", response)