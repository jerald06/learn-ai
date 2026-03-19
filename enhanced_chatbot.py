"""
Enhanced AI Chatbot with MCP integration and proper configuration management.
Combines vector database knowledge with MySQL user data via MCP tools.
"""

from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.agents import initialize_agent, Tool
from langchain.memory import ConversationBufferMemory
from typing import Dict, Any
import json

from config import config
from database import user_repository


class VectorKnowledgeBase:
    """Manages vector database for knowledge base operations."""
    
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL
        )
        self.db = Chroma(
            persist_directory=config.VECTOR_DB_PATH,
            embedding_function=self.embeddings
        )
        self.retriever = self.db.as_retriever()
        self.qa_chain = load_qa_chain(
            Ollama(model=config.OLLAMA_MODEL, base_url=config.OLLAMA_BASE_URL),
            chain_type="stuff"
        )
    
    def search(self, query: str) -> str:
        """Search knowledge base for relevant information."""
        try:
            docs = self.retriever.get_relevant_documents(query)
            return self.qa_chain.run(input_documents=docs, question=query)
        except Exception as e:
            return f"Knowledge base search error: {str(e)}"


class MCPTools:
    """MCP tools for database operations."""
    
    def __init__(self):
        self.user_repo = user_repository
    
    def get_user(self, user_id: str) -> str:
        """Get user details by userId."""
        try:
            user_id = int(user_id)
            user_data = self.user_repo.get_user_by_id(user_id)
            return json.dumps(user_data, indent=2, default=str)
        except ValueError:
            return json.dumps({"error": "Invalid user ID format"})
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def list_users(self, _: str = "") -> str:
        """Get all users."""
        try:
            users = self.user_repo.get_all_users()
            return json.dumps(users, indent=2, default=str)
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def get_high_risk_users(self, _: str = "") -> str:
        """Get high-risk users (credit score < 650)."""
        try:
            users = self.user_repo.get_high_risk_users()
            return json.dumps(users, indent=2, default=str)
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def get_users_with_multiple_loans(self, _: str = "") -> str:
        """Get users with multiple loans."""
        try:
            users = self.user_repo.get_users_with_multiple_loans()
            return json.dumps(users, indent=2, default=str)
        except Exception as e:
            return json.dumps({"error": str(e)})


class EnhancedChatbot:
    """Enhanced AI chatbot with MCP integration."""
    
    def __init__(self):
        # Initialize components
        self.llm = Ollama(model=config.OLLAMA_MODEL, base_url=config.OLLAMA_BASE_URL)
        self.knowledge_base = VectorKnowledgeBase()
        self.mcp_tools = MCPTools()
        
        # Create memory for conversation
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        # Define tools for the agent
        self.tools = [
            Tool(
                name="get_user",
                description="Get user details by userId. Use this when user asks about specific user information.",
                func=self.mcp_tools.get_user
            ),
            Tool(
                name="list_users",
                description="Get all users from the database. Use this when user asks to see all users.",
                func=self.mcp_tools.list_users
            ),
            Tool(
                name="get_high_risk_users",
                description="Get users with creditScore below 650. Use this when user asks about high-risk users or low credit scores.",
                func=self.mcp_tools.get_high_risk_users
            ),
            Tool(
                name="get_users_with_multiple_loans",
                description="Get users with more than 1 existing loan. Use this when user asks about users with multiple loans.",
                func=self.mcp_tools.get_users_with_multiple_loans
            ),
            Tool(
                name="search_knowledge",
                description="Search the knowledge base for information about company, services, policies, etc.",
                func=self.knowledge_base.search
            )
        ]
        
        # Initialize the agent
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent="conversational-react-description",
            memory=self.memory,
            verbose=True
        )
    
    def run(self, query: str) -> str:
        """Process user query and return response."""
        try:
            response = self.agent.run(query)
            return response
        except Exception as e:
            return f"Error processing query: {str(e)}"
    
    def test_system(self) -> Dict[str, Any]:
        """Test all system components."""
        results = {}
        
        # Test database connection
        results["database"] = user_repository.db_manager.test_connection()
        
        # Test user count
        try:
            user_count = user_repository.get_user_count()
            results["user_count"] = user_count
        except Exception as e:
            results["user_count_error"] = str(e)
        
        # Test knowledge base
        try:
            kb_response = self.knowledge_base.search("test")
            results["knowledge_base"] = "working" if kb_response else "empty"
        except Exception as e:
            results["knowledge_base_error"] = str(e)
        
        return results


# Create global chatbot instance
chatbot = EnhancedChatbot()

# Create a wrapper for backward compatibility
qa = chatbot


# CLI version for testing
if __name__ == "__main__":
    print("🤖 Enhanced AI Assistant with MCP MySQL Integration")
    print("=" * 50)
    
    # Test system
    print("🔍 Testing system components...")
    test_results = chatbot.test_system()
    
    for component, status in test_results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {component}: {status}")
    
    print("\n📝 Available commands:")
    print("- Get user 1001 details")
    print("- List all users")
    print("- Show high-risk users")
    print("- Who has multiple loans?")
    print("- Any question about your knowledge base")
    print("Type 'quit' to exit\n")
    
    while True:
        try:
            query = input("You: ")
            if query.lower() in ['quit', 'exit', 'q']:
                break
            
            response = chatbot.run(query)
            print(f"Bot: {response}")
            print()
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
