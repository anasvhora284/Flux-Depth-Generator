import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        
        /* Button primary */
        .stButton > button {
            background-color: #238636;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: background-color 0.2s;
            width: 100%;
        }
        .stButton > button:hover {
            background-color: #2ea043;
        }
        
        /* Header */
        .header-container {
            padding: 3rem 0 2rem 0;
            text-align: center;
        }
        .header-title {
            font-size: 3rem;
            font-weight: 700;
            background: -webkit-linear-gradient(45deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        .header-subtitle {
            color: #8b949e;
            font-size: 1.2rem;
            font-weight: 400;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 2rem;
            color: #8b949e;
            font-size: 0.85rem;
            border-top: 1px solid #30363d;
            margin-top: 4rem;
        }
        
        /* Upload box customization */
        [data-testid="stFileUploader"] {
            padding: 2rem;
            border: 1px dashed #30363d;
            border-radius: 12px;
            background-color: #161b22;
        }
        </style>
    """, unsafe_allow_html=True)

def render_header():
    st.markdown("""
        <div class="header-container">
            <div class="header-title">Depth Generator Pro</div>
            <div class="header-subtitle">Turn flat images into immersive 3D depth maps instantly.</div>
        </div>
    """, unsafe_allow_html=True)

def render_footer():
    st.markdown("""
        <div class="footer">
            Built with Depth Anything V2 • Streamlit • PyTorch
        </div>
    """, unsafe_allow_html=True)
