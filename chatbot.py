from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

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
qa_chain = load_qa_chain(llm, chain_type="stuff")

# Create a wrapper function to maintain compatibility
class QAWrapper:
    def __init__(self, chain, retriever):
        self.chain = chain
        self.retriever = retriever
    
    def run(self, query):
        docs = self.retriever.get_relevant_documents(query)
        return self.chain.run(input_documents=docs, question=query)

qa = QAWrapper(qa_chain, retriever)

# Uncomment the following lines if you want to run the CLI version separately
# while True:
#     query = input("Ask: ")
#     response = qa.run(query)
#     print("Bot:", response)