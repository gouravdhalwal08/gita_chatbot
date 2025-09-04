import json
import faiss
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# File paths
INDEX_FILE = "data/index.faiss"
META_FILE = "data/metadata.json"

# --- Load Models and Data ---
print("🔄 Loading models and data...")
# Load FAISS index
index = faiss.read_index(INDEX_FILE)

# Load metadata
with open(META_FILE, "r", encoding="utf-8") as f:
    verses = json.load(f)

# Load the SAME embedding model used for building the index
embedder = SentenceTransformer("BAAI/bge-base-en-v1.5")

# Load HuggingFace LLM. Consider a slightly larger model if you have the resources.
# 'google/flan-t5-large' is a good step up. If not, 'flan-t5-base' is fine.
llm = pipeline("text2text-generation", model="google/flan-t5-base")
print("✅ Models loaded.")

def search(query, top_k=5): # Increased top_k to 5 for more context
    """Find most relevant shlokas based on semantic meaning."""
    # For BGE models, it's recommended to add an instruction to the query.
    query_with_instruction = f"Represent this question for searching relevant passages: {query}"
    q_emb = embedder.encode([query_with_instruction], convert_to_numpy=True)
    D, I = index.search(q_emb.astype('float32'), top_k)
    
    context = []
    for idx in I[0]:
        verse = verses[idx]
        context.append(
            f"From Bhagavad Gita {verse['chapter']}.{verse['verse']}: {verse['translation_en']}\nExplanation: {verse['explanation_en']}"
        )
    return "\n\n".join(context)

def chatbot(query):
    """Generate an answer using the LLM with improved prompting."""
    context = search(query)

    # This is a much more detailed "System Prompt"
    prompt = f"""
    You are a wise and compassionate spiritual guide, embodying the persona of Lord Krishna from the Bhagavad Gita.
    Your purpose is to provide profound, yet simple and actionable guidance to a person who is suffering or confused.
    
    You have been provided with relevant verses and explanations from the Bhagavad Gita as context.
    Your answer MUST be based ONLY on the provided context. Do not use any external knowledge.
    
    Follow these instructions carefully:
    1.  Begin your answer by addressing the user with warmth and understanding, like "My dear friend," or "O seeker of truth,".
    2.  Synthesize the key message from the provided verses. Do not just repeat them.
    3.  Explain the principle in a simple, practical way that the user can apply to their life.
    4.  Maintain a tone that is serene, reassuring, and full of wisdom.
    5.  Conclude with a blessing or an encouraging closing remark.
    
    Here are the relevant verses for your reference:
    ---
    CONTEXT:
    {context}
    ---
    
    Now, please answer the user's question with compassion and wisdom.
    
    QUESTION: {query}
    
    ANSWER:
    """

    response = llm(prompt, max_length=512, do_sample=True, temperature=0.7)
    return response[0]['generated_text']

if __name__ == "__main__":
    print("\n🕉 Welcome to GitaBot (Improved Version) 🙏")
    while True:
        user_q = input("\n❓ Ask your question: ")
        if user_q.lower() in ["exit", "quit"]:
            break
        ans = chatbot(user_q)
        print("\n✨ GitaBot:", ans)