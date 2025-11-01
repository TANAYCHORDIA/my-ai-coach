import os
import pickle
import numpy as np
import faiss
import google.generativeai as genai
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pathlib import Path # <<< NEW IMPORT

# ==========================================
# Simple Text Splitter (No change needed)
# ==========================================
class SimpleTextSplitter:
    """Splits text into overlapping chunks for embedding & retrieval"""
    def __init__(self, chunk_size=500, chunk_overlap=50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text):
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start += self.chunk_size - self.chunk_overlap
        return chunks


# ==========================================
# Main Coach Carter AI Engine
# ==========================================
class CoachCarterAI:
    """
    Hybrid AI Brain:
    - SentenceTransformer + FAISS for embeddings (local)
    - Google Gemini for response generation (cloud)
    """

    def __init__(self, rebuild_embeddings=False):
        print("🧠 Initializing Coach Carter Hybrid AI...")

        # --- PATH DEFINITION (New Absolute Path Logic) ---
        # Get the absolute path to the directory containing this script (backend/app)
        self.APP_DIR = Path(__file__).parent 
        # Get the absolute path to the data folder (backend/data)
        self.DATA_DIR = self.APP_DIR.parent / "data" 
        # Create data directory if it doesn't exist
        os.makedirs(self.DATA_DIR, exist_ok=True) 
        # --- END PATH DEFINITION ---

        # Step 1: Load API key
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("❌ GEMINI_API_KEY not found in .env")

        genai.configure(api_key=self.api_key)
        print(f"✅ Google API key loaded: {self.api_key[:10]}...")

        # Step 2: Initialize models
        print("📚 Loading local embedding model (SentenceTransformer)...")
        self.embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        print("🤖 Loading Gemini model (for responses)...")
        self.llm = genai.GenerativeModel("gemini-2.0-flash")

        # Step 3: Load or build knowledge base
        print("📖 Loading expert knowledge base...")
        # Pass the force_new flag to the loader
        self.vector_store = self._load_or_build_knowledge_base(force_new=rebuild_embeddings) 
        print("✅ Coach Carter is ready!\n")

    # ==========================================
    # Knowledge Base Builder / Loader (UPDATED)
    # ==========================================
    def _load_or_build_knowledge_base(self, force_new=False):
        """
        Loads saved FAISS embeddings if they exist,
        else rebuilds them and saves for reuse.
        Uses absolute paths defined in __init__.
        """
        # --- ABSOLUTE PATHS ---
        faiss_path = self.DATA_DIR / "faiss_index.bin"
        meta_path = self.DATA_DIR / "vector_meta.pkl"
        text_path = self.DATA_DIR / "expert_knowledge.txt"
        # --- END ABSOLUTE PATHS ---

        # --- Load from cache ---
        if not force_new and faiss_path.exists() and meta_path.exists():
            print("   ✅ Found saved FAISS embeddings. Loading...")
            index = faiss.read_index(str(faiss_path)) # FAISS needs a string path
            with open(meta_path, "rb") as f:
                meta = pickle.load(f)
            print("   ✅ Loaded embeddings from cache")
            return {
                "index": index,
                "chunks": meta["chunks"],
                "embeddings": meta["embeddings"]
            }

        # --- Rebuild from text ---
        if not text_path.exists():
            print("⚠️  expert_knowledge.txt not found at absolute path! Using empty base.")
            return None

        with open(text_path, "r", encoding="utf-8") as f:
            text = f.read()

        splitter = SimpleTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_text(text)
        print(f"   ✅ Split into {len(chunks)} chunks")

        embeddings = self.embedding_model.encode(chunks, convert_to_numpy=True, show_progress_bar=True)

        # Build FAISS index
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)
        print("   ✅ FAISS vector database created")

        # Save for reuse
        faiss.write_index(index, str(faiss_path)) # FAISS needs a string path
        with open(meta_path, "wb") as f:
            pickle.dump({"chunks": chunks, "embeddings": embeddings}, f)
        print("   💾 Saved FAISS index and embeddings for future use")

        return {"index": index, "chunks": chunks, "embeddings": embeddings}

    # ==========================================
    # Remaining methods are unchanged:
    # _retrieve_context, _build_prompt, get_ai_response
    # ==========================================
    def _retrieve_context(self, query, top_k=3):
        # ... (unchanged)
        if not self.vector_store:
            return ""

        query_emb = self.embedding_model.encode([query], convert_to_numpy=True)
        distances, indices = self.vector_store["index"].search(query_emb, top_k)
        results = [self.vector_store["chunks"][i] for i in indices[0]]
        return "\n\n".join(results)

    def _build_prompt(self, user_query, mode="in-depth", context="", user_profile=None):
        # ... (unchanged)
        if mode == "quick":
            system_instruction = (
                "You are Coach Carter, a friendly AI fitness coach.\n"
                "🎯 QUICK TIP MODE: Give concise, actionable advice (2–3 sentences, <150 words)."
            )
        else:
            system_instruction = (
                "You are Coach Carter, an elite sports coach with 20+ years of experience.\n"
                "🎯 IN-DEPTH PLAN MODE: Create complete, structured training programs.\n"
                "Use markdown formatting with sections like:\n"
                "- Program Overview\n"
                "- Weekly Breakdown\n"
                "- Warm-up & Cool-down\n"
                "- Progression Plan\n"
                "- Safety Notes"
            )

        profile_text = ""
        if user_profile:
            profile_text = f"\n\nUSER PROFILE:\n{user_profile}\n"

        return (
            f"{system_instruction}\n\n"
            f"Relevant Knowledge:\n{context}\n\n"
            f"User Question: {user_query}\n"
            f"{profile_text}\n"
            f"Your Response:"
        )

    def get_ai_response(self, user_query, mode="in-depth", user_profile=None):
        # ... (unchanged)
        print(f"\n💬 Processing query: {user_query[:80]}...")

        context = self._retrieve_context(user_query)
        prompt = self._build_prompt(user_query, mode, context, user_profile)

        response = self.llm.generate_content(prompt)
        print("✅ Response generated!\n")
        return response.text


# ==========================================
# Command-line and Helper (No change needed)
# ==========================================
if __name__ == "__main__":
    import sys

    rebuild = "--new" in sys.argv
    print("=" * 60)
    # The CoachCarterAI class now handles the pathing correctly
    coach_ai = CoachCarterAI(rebuild_embeddings=rebuild) 
    print("=" * 60)

    # Example usage
    answer = coach_ai.get_ai_response("Create a 4-week fat loss plan for beginners.")
    print("\n🗣️ Response:\n", answer)
else:
    # If imported, initialize once
    coach_ai = CoachCarterAI()


def get_ai_response(user_query: str, mode: str = "in-depth", user_profile: dict = None):
    """Helper for external use"""
    return coach_ai.get_ai_response(user_query, mode, user_profile)