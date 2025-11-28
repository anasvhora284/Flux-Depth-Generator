import streamlit as st
from src.config import get_theme_colors, save_settings, load_settings, resolve_theme

def inject_custom_css(theme_mode="dark", accent_color="#238636"):
    """Inject custom CSS with theme support."""
    colors = get_theme_colors(theme_mode)
    
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Root variables */
        :root {{
            --bg-primary: {colors['bg_primary']};
            --bg-secondary: {colors['bg_secondary']};
            --bg-tertiary: {colors['bg_tertiary']};
            --text-primary: {colors['text_primary']};
            --text-secondary: {colors['text_secondary']};
            --border: {colors['border']};
            --accent: {accent_color};
            --success: {colors['success']};
            --card-bg: {colors['card_bg']};
            --card-border: {colors['card_border']};
            --input-bg: {colors['input_bg']};
        }}
        
        /* Base styles */
        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        
        .stApp {{
            background-color: var(--bg-primary);
            color: var(--text-primary);
            transition: all 0.3s ease;
        }}
        
        /* Glassmorphism cards */
        .glass-card {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }}
        
        .glass-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
        }}
        
        /* Enhanced buttons */
        .stButton > button {{
            background: linear-gradient(135deg, var(--accent) 0%, var(--success) 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            width: 100%;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            cursor: pointer;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
        }}
        
        .stButton > button:active {{
            transform: translateY(0);
        }}
        
        /* Header */
        .header-container {{
            padding: 3rem 0 2rem 0;
            text-align: center;
            position: relative;
        }}
        
        .header-title {{
            font-size: 3.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
            animation: gradient-shift 3s ease infinite;
            background-size: 200% 200%;
        }}
        
        @keyframes gradient-shift {{
            0%, 100% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
        }}
        
        .header-subtitle {{
            color: var(--text-secondary);
            font-size: 1.2rem;
            font-weight: 400;
            max-width: 600px;
            margin: 0 auto;
        }}
        
        .theme-badge {{
            position: absolute;
            top: 1rem;
            right: 1rem;
            padding: 0.5rem 1rem;
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 20px;
            font-size: 0.85rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        /* Stats card */
        .stats-card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
        }}
        
        .stat-value {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--accent);
        }}
        
        .stat-label {{
            font-size: 0.85rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        /* Upload zone */
        [data-testid="stFileUploader"] {{
            padding: 3rem;
            border: 2px dashed var(--border);
            border-radius: 16px;
            background: var(--card-bg);
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        
        [data-testid="stFileUploader"]:hover {{
            border-color: var(--accent);
            background: var(--input-bg);
            transform: scale(1.02);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        }}
        
        /* Progress bars */
        .stProgress > div > div > div {{
            background: linear-gradient(90deg, var(--accent), var(--success));
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }}
        
        /* Image preview grid */
        .preview-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }}
        
        .preview-item {{
            position: relative;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid var(--border);
            transition: all 0.3s ease;
        }}
        
        .preview-item:hover {{
            transform: scale(1.05);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
        }}
        
        /* Comparison slider */
        .comparison-container {{
            position: relative;
            width: 100%;
            overflow: hidden;
            border-radius: 12px;
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding: 3rem 2rem;
            color: var(--text-secondary);
            font-size: 0.9rem;
            border-top: 1px solid var(--border);
            margin-top: 4rem;
        }}
        
        .footer-links {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-top: 1rem;
        }}
        
        .footer-link {{
            color: var(--text-secondary);
            text-decoration: none;
            transition: color 0.2s;
        }}
        
        .footer-link:hover {{
            color: var(--accent);
        }}
        
        /* Metrics display */
        .metric-row {{
            display: flex;
            gap: 1rem;
            margin: 1rem 0;
        }}
        
        .metric-box {{
            flex: 1;
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
        }}
        
        /* Badges */
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            background: var(--accent);
            color: white;
        }}
        
        /* Sidebar enhancements */
        [data-testid="stSidebar"] {{
            background: var(--bg-secondary);
            border-right: 1px solid var(--border);
        }}
        
        /* Selectbox and inputs */
        .stSelectbox, .stSlider {{
            margin: 0.5rem 0;
        }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0.5rem;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            border-radius: 8px 8px 0 0;
            padding: 0.5rem 1.5rem;
        }}
        
        /* Expander */
        .streamlit-expanderHeader {{
            background: var(--card-bg);
            border-radius: 8px;
        }}
        
        /* Animations */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .fade-in {{
            animation: fadeIn 0.5s ease;
        }}
        
        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 10px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: var(--bg-secondary);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: var(--border);
            border-radius: 5px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: var(--accent);
        }}
        </style>
    """, unsafe_allow_html=True)

def render_header(theme_mode="dark"):
    """Render the application header with theme toggle and indicator."""
    theme_icon = "🌙" if theme_mode == "dark" else "☀️"
    
    # Create two columns for header
    col1, col2 = st.columns([10, 1])
    
    with col1:
        st.markdown(f"""
            <div class="header-container">
                <div class="header-title">✨ Depth Generator Pro</div>
                <div class="header-subtitle">Transform flat images into immersive 3D depth maps with AI-powered precision</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Theme toggle button
        if st.button(f"{theme_icon}", help="Toggle light/dark mode", key="theme_toggle"):
            settings = load_settings()
            current_theme = resolve_theme(settings)
            new_theme = "light" if current_theme == "dark" else "dark"
            settings["user_theme_preference"] = new_theme
            save_settings(settings)
            st.rerun()

def render_footer():
    """Render the application footer."""
    st.markdown("""
        <div class="footer">
            <div>Built with ❤️ using Depth Anything V2 • Streamlit • PyTorch</div>
            <div class="footer-links">
                <a href="https://github.com/DepthAnything/Depth-Anything-V2" class="footer-link" target="_blank">📚 Documentation</a>
                <a href="https://github.com" class="footer-link" target="_blank">🐙 GitHub</a>
                <a href="#" class="footer-link">⚙️ Settings</a>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_metric_card(label, value, icon="📊"):
    """Render a metric card."""
    st.markdown(f"""
        <div class="stats-card">
            <div class="stat-label">{icon} {label}</div>
            <div class="stat-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)

def render_badge(text, color="accent"):
    """Render a badge."""
    return f'<span class="badge" style="background: var(--{color});">{text}</span>'
