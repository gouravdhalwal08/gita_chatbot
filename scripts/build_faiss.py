import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

# Paths
DATA_FILE = "data/gita_full.json"
INDEX_FILE = "data/index.faiss"
META_FILE = "data/metadata.json"

# Load data
with open(DATA_FILE, "r", encoding="utf-8") as f:
    verses = json.load(f)

# --- UPGRADE ---
# Hum ek behtar, multi-lingual model ka istemal karenge.
# Yeh model Hindi, English, aur Sanskrit ke anuvaad ko samajh sakta hai.
print("🔄 Loading embedding model (paraphrase-multilingual-mpnet-base-v2)...")
model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")

# Prepare text corpus (Combine all relevant text for better search)
texts = []
for v in verses:
    chapter = v.get("chapter", "")
    verse = v.get("verse", "")
    sanskrit = v.get("sanskrit", "")
    transliteration = v.get("transliteration", "")
    translation_en = v.get("translation_en", "")
    explanation_en = v.get("explanation_en", "")

    # Hum sab kuch jodenge taaki search har cheez par ho sake
    combined = (
        f"Chapter {chapter}, Verse {verse}. "
        f"In Sanskrit: {sanskrit}. "
        f"Pronounced as: {transliteration}. "
        f"Meaning in English: {translation_en}. "
        f"Explanation: {explanation_en}"
    )
    texts.append(combined)

# Encode
print("🔄 Encoding verses...")
embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

# Create FAISS index
d = embeddings.shape[1]  # embedding dimensions
index = faiss.IndexFlatL2(d)
index.add(embeddings.astype('float32')) # Ensure float32 for FAISS

# Save index
Path("data").mkdir(parents=True, exist_ok=True)
faiss.write_index(index, INDEX_FILE)

# Save metadata
with open(META_FILE, "w", encoding="utf-8") as f:
    json.dump(verses, f, ensure_ascii=False, indent=2)

print(f"✅ FAISS index built with {index.ntotal} verses using a multi-lingual model.")
