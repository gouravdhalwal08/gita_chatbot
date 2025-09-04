import faiss
import json
import os
from sentence_transformers import SentenceTransformer

# --- 1. Define File Paths ---
INDEX_FILE = "data/index.faiss"
META_FILE = "data/metadata.json"

# --- 2. Add Diagnostic and Error Handling ---
# Check if the data files exist before trying to load them
if not os.path.exists(INDEX_FILE) or not os.path.exists(META_FILE):
    print(f"Error: Required data files not found.")
    print(f"Please ensure '{os.path.abspath(INDEX_FILE)}' and '{os.path.abspath(META_FILE)}' exist.")
    exit()

try:
    # --- 3. Load FAISS Index and Metadata ---
    index = faiss.read_index(INDEX_FILE)
    print(f"Successfully loaded FAISS index with {index.ntotal} vectors.")

    with open(META_FILE, "r", encoding="utf-8") as f:
        verses = json.load(f)
    print(f"Successfully loaded {len(verses)} verses from metadata.")

except Exception as e:
    print(f"Error loading files: {e}")
    exit()

# --- 4. Load Embedding Model ---
model = SentenceTransformer("all-MiniLM-L6-v2")

# --- 5. Define the Search Function ---
# The function now has a flexible `top_k` parameter
def search(query, top_k=3):
    """
    Performs a semantic search on the FAISS index for a given query.
    
    Args:
        query (str): The search query.
        top_k (int): The number of top results to return.
    
    Returns:
        list: A list of formatted strings, each containing a matching verse.
    """
    q_emb = model.encode([query], convert_to_numpy=True)
    D, I = index.search(q_emb, top_k)
    
    results = []
    print(f"Indices returned by FAISS: {I[0]}") # Debugging line
    
    for idx in I[0]:
        # Check if the returned index is valid
        if 0 <= idx < len(verses):
            verse = verses[idx]
            results.append(
                f"📖 Chapter {verse['chapter']}, Verse {verse['verse']}\n"
                f"🕉 Sanskrit: {verse['sanskrit']}\n"
                f"🌍 English: {verse['translation_en']}\n"
            )
        else:
            print(f"Warning: Invalid index {idx} returned by FAISS. Skipping.")
            
    return results

# --- 6. Example Test with Flexible `top_k` ---
if __name__ == "__main__":
    
    # Example 1: Query about "duty" with a higher top_k
    query_duty = "What does Krishna say about duty?"
    print(f"\n🔍 Query: {query_duty}")
    print("----------------------------------------")
    print("Requesting top 5 most relevant verses:")
    for res in search(query_duty, top_k=5):
        print(res)

    # Example 2: Query about the "soul" with a different top_k
    query_soul = "Describe the nature of the soul"
    print(f"\n🔍 Query: {query_soul}")
    print("----------------------------------------")
    print("Requesting top 10 most relevant verses:")
    for res in search(query_soul, top_k=10):
        print(res)
        
    # Example 3: You can also use the default top_k
    query_karma = "What is Karma?"
    print(f"\n🔍 Query: {query_karma}")
    print("----------------------------------------")
    print("Requesting default top_k=3 verses:")
    for res in search(query_karma):
        print(res)