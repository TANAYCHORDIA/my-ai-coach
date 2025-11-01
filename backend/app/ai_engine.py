
# backend/app/ai_engine.py

import os
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class CoachCarterAI:
    """
    The Brain of Coach Carter - AI Engine with RAG
    """
    
    def __init__(self):
        print("🧠 Initializing Coach Carter AI Brain...")
        
        # Step 1: Get API Key
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("❌ GEMINI_API_KEY not found! Check your .env file")
        
        print(f"✅ API Key loaded: {self.api_key[:10]}...")
        
        # Step 2: Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Step 3: Initialize Embeddings (for RAG)
        print("📚 Loading embeddings model...")
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=self.api_key
        )
        
        # Step 4: Initialize LLM
        print("🤖 Loading Gemini Flash 2.5 model...")
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.api_key,
            temperature=0.7,  # Controls creativity (0 = focused, 1 = creative)
            max_output_tokens=2048
        )
        
        # Step 5: Load Knowledge Base (RAG)
        print("📖 Loading expert knowledge base...")
        self.vector_store = self._load_knowledge_base()
        
        print("✅ Coach Carter AI is ready!\n")
    
    def _load_knowledge_base(self):
        """
        STEP 2: BUILD THE EXPERT LIBRARY (RAG)
        This loads expert_knowledge.txt and creates a searchable vector store
        """
        try:
            # Load the text file
            loader = TextLoader('data/expert_knowledge.txt', encoding='utf-8')
            documents = loader.load()
            print(f"   ✅ Loaded expert_knowledge.txt")
            
            # Split into chunks (smaller pieces for better search)
            text_splitter = CharacterTextSplitter(
                separator="\n\n",  # Split by paragraphs
                chunk_size=500,    # 500 characters per chunk
                chunk_overlap=50   # 50 character overlap for context
            )
            texts = text_splitter.split_documents(documents)
            print(f"   ✅ Split into {len(texts)} knowledge chunks")
            
            # Create FAISS vector store (makes text searchable)
            vector_store = FAISS.from_documents(texts, self.embeddings)
            print(f"   ✅ Created searchable vector database")
            
            return vector_store
        
        except FileNotFoundError:
            print("   ⚠️  expert_knowledge.txt not found! Creating empty knowledge base...")
            return None
        except Exception as e:
            print(f"   ❌ Error loading knowledge: {e}")
            return None
    
    def _build_perfect_prompt(self, user_query: str, mode: str = "in-depth") -> str:
        """
        STEP 3: ENGINEER THE PERFECT PROMPT
        This creates the system instructions for the AI
        """
        
        if mode == "quick":
            system_instruction = """You are Coach Carter, a friendly fitness AI assistant.

🎯 QUICK TIP MODE: Provide brief, actionable advice in 2-3 sentences max.

Rules:
- Keep responses under 150 words
- Be direct and helpful
- Focus on immediate tips"""
        
        else:  # in-depth mode
            system_instruction = """You are Coach Carter, an expert sports training coach with 20+ years of experience.

🎯 IN-DEPTH PLAN MODE: Provide comprehensive, structured training programs.

Your response MUST include these sections:

## 📋 Program Overview
- Duration and frequency
- Target goal

## 🗓️ Weekly Breakdown
**Day 1: [Muscle Group]**
1. Exercise Name (Sets x Reps, Rest)
2. Exercise Name (Sets x Reps, Rest)

**Day 2: [Muscle Group]**
...

## 🔥 Warm-Up Protocol
- List 3-5 warm-up exercises with duration

## ❄️ Cool-Down
- Stretching routine (5-10 minutes)

## 📈 Progression Plan
- How to progress over next 4 weeks

## ⚠️ Safety Notes
- Injury prevention tips
- Form cues

FORMATTING RULES:
✅ Use headings (##) for sections
✅ Use bullet points and numbered lists
✅ Format exercises as: "Exercise Name (Sets x Reps, Rest)"
✅ Be specific with numbers (sets, reps, rest periods)
✅ ALWAYS consider user's injury history if mentioned"""
        
        return system_instruction
    
    def get_ai_response(self, user_query: str, mode: str = "in-depth", user_profile: dict = None) -> str:
        """
        STEP 4: CREATE THE FINAL BRAIN FUNCTION
        This is your main function that ties everything together
        """
        
        print(f"\n💬 Processing query in {mode} mode...")
        print(f"Query: {user_query[:100]}...\n")
        
        try:
            # Build the prompt
            system_instruction = self._build_perfect_prompt(user_query, mode)
            
            # Add user profile context if available
            if user_profile:
                profile_text = f"""
USER PROFILE:
- Goal: {user_profile.get('goal', 'Not specified')}
- Injuries: {', '.join(user_profile.get('injuries', [])) or 'None'}
- Experience: {user_profile.get('experience_level', 'Not specified')}
"""
                system_instruction += f"\n\n{profile_text}"
            
            # Check if we have a knowledge base
            if self.vector_store:
                print("🔍 Searching expert knowledge base...")
                
                # Create retriever (searches the knowledge base)
                retriever = self.vector_store.as_retriever(
                    search_kwargs={"k": 3}  # Get top 3 most relevant chunks
                )
                
                # Create the RAG prompt template
                template = """Use the following expert knowledge to answer the question.
If the knowledge doesn't contain relevant information, use your general fitness expertise.

{system_instruction}

Expert Knowledge:
{context}

User Question: {question}

Your Response:"""
                
                QA_PROMPT = PromptTemplate(
                    template=template,
                    input_variables=["context", "question", "system_instruction"]
                )
                
                # Create the RAG chain
                qa_chain = RetrievalQA.from_chain_type(
                    llm=self.llm,
                    chain_type="stuff",
                    retriever=retriever,
                    chain_type_kwargs={
                        "prompt": QA_PROMPT,
                    }
                )
                
                # Generate response with RAG
                full_prompt = f"{system_instruction}\n\n{user_query}"
                response_text = qa_chain.run(full_prompt)
                print("✅ Response generated with RAG\n")
            
            else:
                # Fallback: Direct LLM call without RAG
                print("⚠️  No knowledge base - using direct LLM call")
                full_prompt = f"{system_instruction}\n\nUser Question: {user_query}"
                response_text = self.llm.predict(full_prompt)
                print("✅ Response generated\n")
            
            return response_text
        
        except Exception as e:
            error_msg = f"❌ Error generating response: {str(e)}"
            print(error_msg)
            return f"I apologize, but I encountered an error: {str(e)}"

# Create global instance
print("=" * 60)
coach_ai = CoachCarterAI()
print("=" * 60)

def get_ai_response(user_query: str, mode: str = "in-depth", user_profile: dict = None) -> str:
    """
    Main function for easy import
    """
    return coach_ai.get_ai_response(user_query, mode, user_profile)
