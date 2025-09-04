🕉️ Gita-Chatbot: The Divine Guide (Local LLM Version)
A beautiful, immersive, and "hallucination-free" chatbot that provides spiritual guidance from the Bhagavad Gita, running completely on your local machine.

This project leverages a powerful RAG (Retrieval-Augmented Generation) architecture to deliver accurate and context-aware answers. The AI brain is a local model from Hugging Face (google/flan-t5-base), ensuring no API keys or internet dependency is required for the core logic. The frontend is a visually stunning Streamlit application designed for a serene and divine user experience.

✨ Key Features
Divine User Interface: A beautiful, dark-themed UI with an animated cosmic background, custom fonts, and immersive design.

Runs Locally: The entire AI logic runs on your computer. No API keys needed, no costs involved.

Streaming Responses: Answers from Krishna appear token-by-token, creating a dynamic and engaging "live" conversation.

Grounded in Wisdom: Uses a strict RAG approach to ensure answers are based only on the provided Gita verses, preventing the AI from generating false information.

Semantic Search: Employs a multi-lingual sentence transformer and a FAISS vector index to find the most relevant shlokas for any user query.

⚙️ How It Works (RAG Architecture)
The chatbot operates on a simple yet powerful two-step process:

Retrieval: When a user asks a question, the sentence-transformer model converts it into a numerical vector. This vector is then used to perform a super-fast similarity search against a pre-indexed FAISS database of all 700 Gita shlokas. The top 2-3 most relevant shlokas are retrieved.

Generation: These retrieved shlokas are then passed as context to a locally-run Language Model (google/flan-t5-base) from Hugging Face. A carefully crafted prompt instructs the model to generate a wise and compassionate answer in the persona of Lord Krishna, strictly based on the provided context.

This RAG approach ensures that the chatbot's answers are always grounded in the actual teachings of the Bhagavad Gita.

🚀 Getting Started
Follow these steps to set up and run the project on your local machine.

1. Prerequisites
Python 3.10 or higher

A virtual environment manager like venv

2. Clone the Repository
git clone [https://github.com/gouravdhalwal08/gita_chatbot.git](https://github.com/gouravdhalwal08/gita_chatbot.git)
cd gita_chatbot

3. Set Up Virtual Environment
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

4. Install Dependencies
All required libraries are listed in backend/requirements.txt.

pip install -r backend/requirements.txt

5. Build the FAISS Vector Index
Before running the app, you need to process the Gita data and create the vector database. This is a one-time step.

python scripts/build_faiss.py

This will create index.faiss and metadata.json inside the data folder.

6. Run the Streamlit Application
You're all set! Run the following command to launch the chatbot. The first time you run this, it may take a few minutes to download the AI models from Hugging Face.

streamlit run app.py
