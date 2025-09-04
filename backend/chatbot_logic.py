import json
import faiss
from sentence_transformers import SentenceTransformer
from transformers import pipeline, TextIteratorStreamer
from threading import Thread
import torch

# --- Configuration ---
INDEX_FILE = "data/index.faiss"
META_FILE = "data/metadata.json"
EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"
# --- THIS LINE IS CORRECTED ---
LLM_MODEL = "google/flan-t5-base"

# --- Global Variables for Models (Load Once) ---
index = None
verses = None
embedder = None
llm = None

def load_models():
    """Loads all models into memory. To be called once at startup."""
    global index, verses, embedder, llm
    
    if index is None:
        print("🔄 Loading FAISS index...")
        index = faiss.read_index(INDEX_FILE)
    
    if verses is None:
        print("🔄 Loading metadata...")
        with open(META_FILE, "r", encoding="utf-8") as f:
            verses = json.load(f)
    
    if embedder is None:
        print("🔄 Loading embedding model...")
        embedder = SentenceTransformer(EMBEDDING_MODEL)
    
    if llm is None:
        print("🔄 Loading Language Model...")
        device = 0 if torch.cuda.is_available() else -1
        llm = pipeline("text2text-generation", model=LLM_MODEL, device=device)
    
    print("✅ All models loaded successfully.")


def search(query, top_k=2):
    """
    Finds the most relevant shlokas and truncates their explanations 
    to ensure the context fits within the model's limit.
    """
    query_with_instruction = f"Represent this question for searching relevant passages: {query}"
    q_emb = embedder.encode([query_with_instruction], convert_to_numpy=True)
    _, I = index.search(q_emb.astype('float32'), top_k)
    
    context = []
    for idx in I[0]:
        verse = verses[idx]
        translation = verse.get('translation_en', '')
        explanation = verse.get('explanation_en', '')

        # --- THIS IS THE FIX ---
        # Truncate the long explanation to keep the context concise for the model.
        # We take the first 300 characters.
        if len(explanation) > 300:
            explanation = explanation[:300] + "..."

        context.append(
            f"From Bhagavad Gita {verse['chapter']}.{verse['verse']}: {translation}\nExplanation: {explanation}"
        )
    return "\n\n".join(context)

# vvv --- CHANGE 2: The entire generate_answer function is rewritten for stability --- vvv
def generate_answer(query):
    """
    Generates a streaming answer. This version uses the model and tokenizer
    directly to bypass a bug in the pipeline's streaming implementation.
    """
    if llm is None:
        raise RuntimeError("Models not loaded. Please call load_models() first.")
    
    context = search(query) 
    
    prompt = f"""
    You are a wise and compassionate spiritual guide, embodying the persona of Lord Krishna. Based ONLY on the provided Bhagavad Gita verses, answer the user's question.

    CONTEXT:
    {context}
    ---
    QUESTION: {query}
    ANSWER:
    """

    # Tokenize the input prompt
    inputs = llm.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512).to(llm.device)
    
    streamer = TextIteratorStreamer(
        llm.tokenizer, 
        skip_prompt=True, 
        skip_special_tokens=True
    )
    
    # Run the generation in a separate thread
    thread = Thread(
        target=llm.model.generate,
        kwargs={
            **inputs,
            "streamer": streamer,
            "max_new_tokens": 350,
            "do_sample": True,
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 50
        }
    )
    thread.start()

    # Yield the tokens as they become available
    for new_text in streamer:
        yield new_text

