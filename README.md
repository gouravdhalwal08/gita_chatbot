# 🕉️ Gita-Chatbot: *The Divine Guide*  

A **free** spiritual chatbot that brings the timeless wisdom of the *Bhagavad Gita* to life — running **completely on your local machine**.  

This project combines **Retrieval-Augmented Generation (RAG)** with a serene **Streamlit frontend**, ensuring responses are always **authentic, grounded, and compassionate**.  

---

## ✨ Features  

- 🎨 **Divine User Interface** – Dark-themed, cosmic background, custom fonts, and immersive design.  
- 💻 **Runs 100% Locally** – No API keys, no internet dependency, and no hidden costs.  
- ⏳ **Streaming Responses** – Lord Krishna’s answers appear **token-by-token**, creating a “live” conversation.  
- 📚 **Grounded in Wisdom** – All answers come directly from the *Bhagavad Gita’s 700 shlokas* using a strict RAG pipeline.  
- 🌍 **Semantic Search** – Multi-lingual sentence-transformer + FAISS index for lightning-fast retrieval of the most relevant verses.  

---

## ⚙️ How It Works – *RAG Architecture*  

The chatbot follows a **two-step process** to ensure divine yet accurate responses:  

1. **Retrieval**  
   - User query → converted into a vector using a sentence-transformer.  
   - FAISS index of all 700 shlokas is searched.  
   - Top **2–3 most relevant verses** are retrieved.  

2. **Generation**  
   - Retrieved shlokas are passed as context to **[google/flan-t5-base](https://huggingface.co/google/flan-t5-base)**.  
   - A carefully designed prompt makes the model answer as *Lord Krishna*, strictly within the retrieved verses.  

✅ This ensures **no hallucinations**, only authentic Gita-based guidance.  

---

## 🚀 Getting Started  

Follow these steps to set up and run the project locally:  

### 1. Prerequisites  
- Python **3.10+**  
- Virtual environment manager (`venv` recommended)  

---

### 2. Clone the Repository  
```bash
git clone https://github.com/gouravdhalwal08/gita_chatbot.git
cd gita_chatbot
3. Set Up Virtual Environment
bash
Copy code
# Create a virtual environment
python3 -m venv .venv  

# Activate the virtual environment
source .venv/bin/activate    # Linux / Mac
.venv\Scripts\activate       # Windows
4. Install Dependencies
All dependencies are listed in backend/requirements.txt:

bash
Copy code
pip install -r backend/requirements.txt
5. Build the FAISS Vector Index
Before running the app, create the vector database (one-time setup):

bash
Copy code
python scripts/build_faiss.py
This generates:

data/index.faiss

data/metadata.json

6. Run the Application
Start the chatbot with Streamlit:

bash
Copy code
streamlit run app.py
⚠️ The first run will download models from Hugging Face. Please be patient.

🖼️ Preview
Here’s what the divine experience looks like:

(Add a screenshot or GIF of your UI here for better presentation)

🙏 Acknowledgements
Bhagavad Gita – Eternal source of wisdom.

Hugging Face – Local LLMs & transformers.

FAISS – Efficient vector similarity search.

Streamlit – Elegant frontend framework.

✨ “Whenever dharma declines and the purpose of life is forgotten, I manifest myself to protect the good, to destroy evil, and to re-establish dharma.” – Bhagavad Gita (4.7–8)

pgsql
Copy code

Do you also want me to **add shields.io badges** (Python, Streamlit, Hugging Face, FAISS) at the to
