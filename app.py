<<<<<<< HEAD
"""
GenZ Slang to Formal English Translator
Streamlit Demo App for NLP Final Project
"""

import streamlit as st
import torch
from transformers import BartTokenizer, BartForConditionalGeneration, pipeline
import os

# ===== Page Configuration =====
st.set_page_config(
    page_title="GenZ Translator",
    page_icon="🗣️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== Custom CSS for Premium Design =====
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Header styling */
    .title-container {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .title-text {
        font-size: 3rem;
        font-weight: 800;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin: 0;
    }
    
    .subtitle-text {
        font-size: 1.2rem;
        color: rgba(255,255,255,0.9);
        margin-top: 0.5rem;
    }
    
    /* Card styling */
    .result-card {
        background: linear-gradient(145deg, #1e3a5f 0%, #2d5a87 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }
    
    .model-label {
        font-size: 0.9rem;
        color: #a0aec0;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .translation-text {
        font-size: 1.3rem;
        color: #e2e8f0;
        line-height: 1.6;
    }
    
    /* Input area styling */
    .stTextArea textarea {
        background: #1e3a5f !important;
        border: 2px solid #667eea !important;
        border-radius: 10px !important;
        color: white !important;
        font-size: 1.1rem !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        padding: 0.8rem 2rem !important;
        border-radius: 50px !important;
        border: none !important;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 30px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Info box */
    .info-box {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Status indicator */
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-loaded {
        background: #48bb78;
        box-shadow: 0 0 10px #48bb78;
    }
    
    .status-error {
        background: #f56565;
        box-shadow: 0 0 10px #f56565;
    }
</style>
""", unsafe_allow_html=True)

# ===== Model Loading =====
@st.cache_resource
def load_models():
    """Load both baseline and proposed models."""
    device = 0 if torch.cuda.is_available() else -1
    models = {}
    
    # Define model paths
    baseline_path = "./bart_baseline_final"
    proposed_path = "./bart_proposed_final"
    
    # Try loading baseline model
    if os.path.exists(baseline_path):
        try:
            models['baseline'] = pipeline(
                "translation", 
                model=baseline_path, 
                tokenizer=baseline_path, 
                device=device
            )
        except Exception as e:
            st.error(f"Error loading baseline model: {e}")
    
    # Try loading proposed model
    if os.path.exists(proposed_path):
        try:
            models['proposed'] = pipeline(
                "translation", 
                model=proposed_path, 
                tokenizer=proposed_path, 
                device=device
            )
        except Exception as e:
            st.error(f"Error loading proposed model: {e}")
    
    return models, device

# ===== Translation Function =====
def translate(text, translator, max_length=128):
    """Translate slang text to formal English."""
    # Add the required prefix
    input_text = f"Translate slang to formal: {text}"
    result = translator(input_text, max_length=max_length)
    return result[0]['translation_text']

# ===== Main App =====
def main():
    # Header
    st.markdown("""
    <div class="title-container">
        <h1 class="title-text">🗣️ GenZ Translator</h1>
        <p class="subtitle-text">Transform GenZ slang into formal English using AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load models
    models, device = load_models()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        # Model status
        st.markdown("#### 📊 Model Status")
        
        if 'baseline' in models:
            st.markdown('<span class="status-indicator status-loaded"></span> Baseline Model ✓', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-indicator status-error"></span> Baseline Model ✗', unsafe_allow_html=True)
        
        if 'proposed' in models:
            st.markdown('<span class="status-indicator status-loaded"></span> Proposed Model ✓', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-indicator status-error"></span> Proposed Model ✗', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Device info
        device_name = "🖥️ GPU (CUDA)" if device == 0 else "💻 CPU"
        st.markdown(f"**Running on:** {device_name}")
        
        st.markdown("---")
        
        # Model selection
        model_choice = st.radio(
            "Select Model",
            options=["Both", "Baseline Only", "Proposed Only"],
            index=0
        )
        
        # Max length slider
        max_length = st.slider("Max Output Length", 32, 256, 128)
        

    
    # Check if models are loaded
    if not models:
        st.warning("⚠️ No models found! Please ensure the model folders exist:")
        st.code("""
./bart_baseline_final/
./bart_proposed_final/
        """)
        st.info("👆 Run the notebook on Colab first, then download the model folders.")
        return
    
    # Main input area
    st.markdown("### 💬 Enter Your Text")
    user_input = st.text_area(
        label="",
        height=150,
        placeholder="Type your GenZ slang here... (e.g., 'ngl that party was lowkey fire fr fr')",
        label_visibility="collapsed"
    )
    
    # Translate button
    col_btn = st.columns([1, 2, 1])
    with col_btn[1]:
        translate_btn = st.button("🚀 Translate", use_container_width=True)
    
    # Results
    if translate_btn and user_input:
        st.markdown("---")
        st.markdown("### 📤 Translation Results")
        
        with st.spinner("Translating..."):
            if model_choice == "Both":
                col_base, col_prop = st.columns(2)
                
                with col_base:
                    if 'baseline' in models:
                        result = translate(user_input, models['baseline'], max_length)
                        st.markdown(f"""
                        <div class="result-card">
                            <div class="model-label">🔷 Baseline (BART)</div>
                            <div class="translation-text">{result}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("Baseline model not loaded")
                
                with col_prop:
                    if 'proposed' in models:
                        result = translate(user_input, models['proposed'], max_length)
                        st.markdown(f"""
                        <div class="result-card">
                            <div class="model-label">🔶 Proposed (Semantic Loss)</div>
                            <div class="translation-text">{result}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("Proposed model not loaded")
            
            elif model_choice == "Baseline Only" and 'baseline' in models:
                result = translate(user_input, models['baseline'], max_length)
                st.markdown(f"""
                <div class="result-card">
                    <div class="model-label">🔷 Baseline (BART)</div>
                    <div class="translation-text">{result}</div>
                </div>
                """, unsafe_allow_html=True)
            
            elif model_choice == "Proposed Only" and 'proposed' in models:
                result = translate(user_input, models['proposed'], max_length)
                st.markdown(f"""
                <div class="result-card">
                    <div class="model-label">🔶 Proposed (Semantic Loss)</div>
                    <div class="translation-text">{result}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #a0aec0; padding: 1rem;">
        <p>NLP Final Project | GenZ Slang to Formal English Translation</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
=======
"""
GenZ Slang to Formal English Translator
Streamlit Demo App for NLP Final Project
"""

import streamlit as st
import torch
from transformers import BartTokenizer, BartForConditionalGeneration, pipeline
import os

# ===== Page Configuration =====
st.set_page_config(
    page_title="GenZ Translator",
    page_icon="🗣️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== Custom CSS for Premium Design =====
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Header styling */
    .title-container {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .title-text {
        font-size: 3rem;
        font-weight: 800;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin: 0;
    }
    
    .subtitle-text {
        font-size: 1.2rem;
        color: rgba(255,255,255,0.9);
        margin-top: 0.5rem;
    }
    
    /* Card styling */
    .result-card {
        background: linear-gradient(145deg, #1e3a5f 0%, #2d5a87 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }
    
    .model-label {
        font-size: 0.9rem;
        color: #a0aec0;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .translation-text {
        font-size: 1.3rem;
        color: #e2e8f0;
        line-height: 1.6;
    }
    
    /* Input area styling */
    .stTextArea textarea {
        background: #1e3a5f !important;
        border: 2px solid #667eea !important;
        border-radius: 10px !important;
        color: white !important;
        font-size: 1.1rem !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        padding: 0.8rem 2rem !important;
        border-radius: 50px !important;
        border: none !important;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 30px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Info box */
    .info-box {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Status indicator */
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-loaded {
        background: #48bb78;
        box-shadow: 0 0 10px #48bb78;
    }
    
    .status-error {
        background: #f56565;
        box-shadow: 0 0 10px #f56565;
    }
</style>
""", unsafe_allow_html=True)

# ===== Model Loading =====
@st.cache_resource
def load_models():
    """Load both baseline and proposed models."""
    device = 0 if torch.cuda.is_available() else -1
    models = {}
    
    # Define model paths
    baseline_path = "./bart_baseline_final"
    proposed_path = "./bart_proposed_final"
    
    # Try loading baseline model
    if os.path.exists(baseline_path):
        try:
            models['baseline'] = pipeline(
                "translation", 
                model=baseline_path, 
                tokenizer=baseline_path, 
                device=device
            )
        except Exception as e:
            st.error(f"Error loading baseline model: {e}")
    
    # Try loading proposed model
    if os.path.exists(proposed_path):
        try:
            models['proposed'] = pipeline(
                "translation", 
                model=proposed_path, 
                tokenizer=proposed_path, 
                device=device
            )
        except Exception as e:
            st.error(f"Error loading proposed model: {e}")
    
    return models, device

# ===== Translation Function =====
def translate(text, translator, max_length=128):
    """Translate slang text to formal English."""
    # Add the required prefix
    input_text = f"Translate slang to formal: {text}"
    result = translator(input_text, max_length=max_length)
    return result[0]['translation_text']

# ===== Main App =====
def main():
    # Header
    st.markdown("""
    <div class="title-container">
        <h1 class="title-text">🗣️ GenZ Translator</h1>
        <p class="subtitle-text">Transform GenZ slang into formal English using AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load models
    models, device = load_models()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        # Model status
        st.markdown("#### 📊 Model Status")
        
        if 'baseline' in models:
            st.markdown('<span class="status-indicator status-loaded"></span> Baseline Model ✓', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-indicator status-error"></span> Baseline Model ✗', unsafe_allow_html=True)
        
        if 'proposed' in models:
            st.markdown('<span class="status-indicator status-loaded"></span> Proposed Model ✓', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-indicator status-error"></span> Proposed Model ✗', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Device info
        device_name = "🖥️ GPU (CUDA)" if device == 0 else "💻 CPU"
        st.markdown(f"**Running on:** {device_name}")
        
        st.markdown("---")
        
        # Model selection
        model_choice = st.radio(
            "Select Model",
            options=["Both", "Baseline Only", "Proposed Only"],
            index=0
        )
        
        # Max length slider
        max_length = st.slider("Max Output Length", 32, 256, 128)
        

    
    # Check if models are loaded
    if not models:
        st.warning("⚠️ No models found! Please ensure the model folders exist:")
        st.code("""
./bart_baseline_final/
./bart_proposed_final/
        """)
        st.info("👆 Run the notebook on Colab first, then download the model folders.")
        return
    
    # Main input area
    st.markdown("### 💬 Enter Your Text")
    user_input = st.text_area(
        label="",
        height=150,
        placeholder="Type your GenZ slang here... (e.g., 'ngl that party was lowkey fire fr fr')",
        label_visibility="collapsed"
    )
    
    # Translate button
    col_btn = st.columns([1, 2, 1])
    with col_btn[1]:
        translate_btn = st.button("🚀 Translate", use_container_width=True)
    
    # Results
    if translate_btn and user_input:
        st.markdown("---")
        st.markdown("### 📤 Translation Results")
        
        with st.spinner("Translating..."):
            if model_choice == "Both":
                col_base, col_prop = st.columns(2)
                
                with col_base:
                    if 'baseline' in models:
                        result = translate(user_input, models['baseline'], max_length)
                        st.markdown(f"""
                        <div class="result-card">
                            <div class="model-label">🔷 Baseline (BART)</div>
                            <div class="translation-text">{result}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("Baseline model not loaded")
                
                with col_prop:
                    if 'proposed' in models:
                        result = translate(user_input, models['proposed'], max_length)
                        st.markdown(f"""
                        <div class="result-card">
                            <div class="model-label">🔶 Proposed (Semantic Loss)</div>
                            <div class="translation-text">{result}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("Proposed model not loaded")
            
            elif model_choice == "Baseline Only" and 'baseline' in models:
                result = translate(user_input, models['baseline'], max_length)
                st.markdown(f"""
                <div class="result-card">
                    <div class="model-label">🔷 Baseline (BART)</div>
                    <div class="translation-text">{result}</div>
                </div>
                """, unsafe_allow_html=True)
            
            elif model_choice == "Proposed Only" and 'proposed' in models:
                result = translate(user_input, models['proposed'], max_length)
                st.markdown(f"""
                <div class="result-card">
                    <div class="model-label">🔶 Proposed (Semantic Loss)</div>
                    <div class="translation-text">{result}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #a0aec0; padding: 1rem;">
        <p>NLP Final Project | GenZ Slang to Formal English Translation</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
>>>>>>> 8b1268f7f5ee6390b24369c588604e34d9904bc1
