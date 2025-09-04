import streamlit as st
from backend import chatbot_logic as bot
import streamlit.components.v1 as components
import base64

# --- IMAGE HELPER FUNCTION ---
# Yeh function image ko Base64 mein convert karta hai taaki use CSS mein daal sakein
@st.cache_data
def get_img_as_base64(file):
    """Reads an image file and converts it to a base64 encoded string."""
    try:
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        st.error(f"Image file not found: {file}")
        return ""

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Gita-Chatbot | The Divine Guide",
    page_icon="🦚",
    layout="wide",
    initial_sidebar_state="auto",
)

# --- LOAD IMAGES ---
# Hum dono images ke path yahan define karte hain
img_krishna_arjuna_path = "/home/gourav_dhalwal/gita-chatbot/assets/krishna_arjuna.png"
img_mb_path = "/home/gourav_dhalwal/gita-chatbot/assets/mb.png"

# Background image ko Base64 mein convert karte hain
img_krishna_arjuna_base64 = get_img_as_base64(img_krishna_arjuna_path)


# --- ADVANCED STYLING & FONT INJECTION ---
# Hum f-string ka istemal karke Base64 image ko seedhe CSS mein daal rahe hain
st.markdown(f"""
<style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Prata&family=Sarabun:wght@300;400&display=swap');

    :root {{
        --primary-bg: #0c0c1d; /* Deep Space Blue */
        --secondary-bg: rgba(22, 22, 46, 0.6); /* Glassmorphism Panel */
        --accent-gold: #ffc971; /* Rich Gold */
        --accent-peacock: #4a9d9c; /* Peacock Blue/Green */
        --text-primary: #f0f0f0;
        --text-secondary: #c0c0c0;
        --font-header: 'Prata', serif;
        --font-body: 'Sarabun', sans-serif;
        --border-color: rgba(255, 201, 113, 0.3);
    }}

    /* Main App Styling */
    .stApp {{
        background-color: var(--primary-bg);
        color: var(--text-primary);
    }}
    
    /* Hide Streamlit's default elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    /* Custom containers for layout */
    .hero-container {{
        position: relative;
        height: 100vh;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 0 1rem;
        /* YAHAN PAR BASE64 IMAGE ADD KI GAYI HAI */
        background-image: linear-gradient(rgba(12, 12, 29, 0.6), rgba(12, 12, 29, 0.8)), url('data:image/png;base64,{img_krishna_arjuna_base64}');
        background-size: cover;
        background-position: center;
    }}
    .hero-content h1 {{
        font-family: var(--font-header);
        font-size: clamp(2.5rem, 8vw, 5rem);
        color: white;
        text-shadow: 0 0 20px var(--accent-gold);
        margin-bottom: 0.5rem;
    }}
    .hero-content p {{
        font-size: clamp(1rem, 3vw, 1.5rem);
        color: var(--accent-gold);
    }}
    
    /* Wisdom Cards Styling & Clickability */
    .stButton>button {{
        background: var(--secondary-bg);
        border: 1px solid var(--border-color);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        width: 100%;
        height: 10rem; /* Give cards a fixed height */
        color: var(--text-primary);
        font-family: var(--font-body);
    }}
    .stButton>button:hover {{
        transform: translateY(-10px);
        box-shadow: 0 0 25px rgba(255, 201, 113, 0.3);
        border: 1px solid var(--accent-gold);
        color: var(--accent-gold);
    }}
    
    /* Chat bubble styling */
    .stChatMessage {{
        background: #2a3858;
        border-radius: 18px;
        border: 1px solid var(--border-color);
        backdrop-filter: blur(5px);
    }}
    [data-testid="stChatMessage"][data-testid="chat-message-user"] {{
        background: linear-gradient(135deg, var(--accent-gold), #ffb347);
        color: #1a1a2e;
    }}
    
    /* Center the main content area */
    .main-content {{
        max-width: 1000px;
        margin: 0 auto;
        padding: 4rem 1rem;
    }}
</style>
""", unsafe_allow_html=True)

# --- ANIMATED BACKGROUND COMPONENT ---
components.html("""
    <div id="particles-js" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1;"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        particlesJS("particles-js", {
            "particles":{"number":{"value":40,"density":{"enable":true,"value_area":800}},"color":{"value":"#ffffff"},"shape":{"type":"circle"},"opacity":{"value":0.5,"random":true},"size":{"value":3,"random":true},"line_linked":{"enable":false},"move":{"enable":true,"speed":1,"direction":"none","random":false,"straight":false,"out_mode":"out","bounce":false}},
            "interactivity":{"detect_on":"canvas","events":{"onhover":{"enable":false},"onclick":{"enable":false},"resize":true}},
            "retina_detect":true
        });
    </script>
""", height=0)

# --- MODEL LOADING ---
@st.cache_resource
def load_all_models():
    """Models ko load aur cache karta hai."""
    with st.spinner("Loading spiritual wisdom... Please wait."):
        bot.load_models()
load_all_models()

# --- SIDEBAR ---
with st.sidebar:
    st.title("About the Divine Guide")
    st.markdown("""
    This is your divine companion, inspired by the timeless wisdom of the Bhagavad Gita. 
    
    Lord Krishna's guidance to Arjuna addresses life's deepest questions. Ask anything that troubles your soul.
    """)
    if st.button("Start New Chat", use_container_width=True):
        st.session_state.messages = [] # Clear chat history
        st.rerun() # Rerun the app to reflect the change

# --- HERO SECTION (HEADER) ---
with st.container():
    st.markdown("""
    <div class="hero-container">
        <div class="hero-content">
            <h1>GITA-CHATBOT</h1>
            <p>The Divine Guide for Your Inner Cosmos</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- MAIN CONTENT AREA ---
with st.container():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    # --- WISDOM CARDS SECTION ---
    st.markdown("<h2 style=\"font-family: 'Prata', serif; text-align: center; color: var(--accent-gold);\">Seek Wisdom</h2>", unsafe_allow_html=True)
    
    def handle_example_click(question):
        """Callback to set question in session state for processing."""
        st.session_state.clicked_question = question

    cols = st.columns(3, gap="large")
    with cols[0]:
        st.button("Purpose of Life", on_click=handle_example_click, args=["What is the purpose of life?"], use_container_width=True)
    with cols[1]:
        st.button("Inner Peace", on_click=handle_example_click, args=["How can I find inner peace?"], use_container_width=True)
    with cols[2]:
        st.button("Nature of the Soul", on_click=handle_example_click, args=["What is the nature of the soul?"], use_container_width=True)

    # --- DECORATIVE DIVIDER IMAGE ---
    # Hum yahan doosri image (mb.png) ko display kar rahe hain
    st.image(img_mb_path, use_column_width=True)

    # --- CHAT INTERFACE ---
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Namaste, seeker of truth. Ask, and let the wisdom of the cosmos unfold."}
        ]

    # Process clicked question
    if "clicked_question" in st.session_state and st.session_state.clicked_question:
        prompt = st.session_state.clicked_question
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Clear after processing
        st.session_state.clicked_question = None
        
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Krishna is contemplating..."):
                response_generator = bot.generate_answer(prompt)
                full_response = st.write_stream(response_generator)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        # Rerun to clear the button state and show the new messages immediately
        st.rerun()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input from chat box
    if prompt := st.chat_input("Type your deepest question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Krishna is contemplating..."):
                response_generator = bot.generate_answer(prompt)
                full_response = st.write_stream(response_generator)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

