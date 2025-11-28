import streamlit as st
from src.config import get_theme_colors, save_settings, load_settings, resolve_theme

def inject_custom_css(theme_mode="dark", accent_color="#238636"):
    """Inject custom CSS with comprehensive design system."""
    colors = get_theme_colors(theme_mode)
    
    # Enhanced color system
    if theme_mode == "light":
        primary_gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        accent_gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        processing_color = "#f59e0b"
        success_color = "#10b981"
        error_color = "#ef4444"
        shadow_light = "rgba(0, 0, 0, 0.08)"
        shadow_medium = "rgba(0, 0, 0, 0.12)"
        shadow_heavy = "rgba(0, 0, 0, 0.2)"
    else:
        primary_gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        accent_gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        processing_color = "#fbbf24"
        success_color = "#34d399"
        error_color = "#f87171"
        shadow_light = "rgba(0, 0, 0, 0.3)"
        shadow_medium = "rgba(0, 0, 0, 0.4)"
        shadow_heavy = "rgba(0, 0, 0, 0.6)"
    
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');
        
        /* ===== DESIGN TOKENS ===== */
        :root {{
            /* Colors */
            --primary: #667eea;
            --primary-light: #8b9ef8;
            --primary-dark: #5568d3;
            --secondary: #764ba2;
            --accent: #f59e0b;
            --success: {success_color};
            --processing: {processing_color};
            --error: {error_color};
            --warning: #fbbf24;
            
            /* Semantic colors */
            --bg-primary: {colors['bg_primary']};
            --bg-secondary: {colors['bg_secondary']};
            --bg-tertiary: {colors['bg_tertiary']};
            --text-primary: {colors['text_primary']};
            --text-secondary: {colors['text_secondary']};
            --text-tertiary: {colors.get('text_tertiary', '#999')};
            --border: {colors['border']};
            --card-bg: {colors['card_bg']};
            --card-border: {colors['card_border']};
            --input-bg: {colors['input_bg']};
            
            /* Shadows */
            --shadow-xs: 0 1px 2px {shadow_light};
            --shadow-sm: 0 2px 4px {shadow_light};
            --shadow-md: 0 4px 12px {shadow_medium};
            --shadow-lg: 0 8px 24px {shadow_medium};
            --shadow-xl: 0 12px 48px {shadow_heavy};
            
            /* Spacing */
            --space-xs: 0.25rem;
            --space-sm: 0.5rem;
            --space-md: 1rem;
            --space-lg: 1.5rem;
            --space-xl: 2rem;
            --space-2xl: 3rem;
            
            /* Border Radius */
            --radius-sm: 6px;
            --radius-md: 10px;
            --radius-lg: 14px;
            --radius-xl: 18px;
            --radius-full: 999px;
            
            /* Transitions */
            --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
            --transition-base: 250ms cubic-bezier(0.4, 0, 0.2, 1);
            --transition-slow: 350ms cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        /* ===== BASE STYLES ===== */
        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 700;
            letter-spacing: -0.02em;
            line-height: 1.2;
        }}
        
        .stApp {{
            background-color: var(--bg-primary);
            color: var(--text-primary);
            transition: background-color var(--transition-base), color var(--transition-base);
        }}
        
        /* ===== TYPOGRAPHY ===== */
        .prose {{
            color: var(--text-primary);
        }}
        
        p {{
            line-height: 1.6;
            color: var(--text-secondary);
        }}
        
        small, .text-sm {{
            font-size: 0.875rem;
            color: var(--text-secondary);
        }}
        
        .text-xs {{
            font-size: 0.75rem;
            color: var(--text-tertiary);
        }}
        
        /* ===== CARDS & CONTAINERS ===== */
        .card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: var(--radius-lg);
            padding: var(--space-xl);
            transition: all var(--transition-base);
            box-shadow: var(--shadow-sm);
        }}
        
        .card:hover {{
            border-color: var(--primary);
            box-shadow: var(--shadow-md);
            transform: translateY(-2px);
        }}
        
        .glass-card {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid var(--card-border);
            border-radius: var(--radius-xl);
            padding: var(--space-xl);
            box-shadow: var(--shadow-lg);
            transition: all var(--transition-base);
        }}
        
        .glass-card:hover {{
            border-color: var(--primary);
            box-shadow: var(--shadow-xl);
            transform: translateY(-4px);
        }}
        
        /* ===== BUTTONS ===== */
        .stButton > button {{
            background: {primary_gradient};
            color: white;
            border: none;
            border-radius: var(--radius-lg);
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all var(--transition-base);
            width: 100%;
            box-shadow: var(--shadow-md);
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }}
        
        .stButton > button:active {{
            transform: translateY(0);
            box-shadow: var(--shadow-md);
        }}
        
        .stButton > button:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }}
        
        /* Primary Button */
        .btn-primary {{
            background: {primary_gradient};
            color: white;
        }}
        
        /* Success Button */
        .btn-success {{
            background: linear-gradient(135deg, var(--success) 0%, #059669 100%);
            color: white;
        }}
        
        /* Secondary Button */
        .btn-secondary {{
            background: var(--card-bg);
            border: 2px solid var(--primary);
            color: var(--primary);
        }}
        
        /* ===== INPUTS & FORMS ===== */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select {{
            background-color: var(--input-bg);
            color: var(--text-primary);
            border: 2px solid var(--card-border);
            border-radius: var(--radius-md);
            padding: 0.75rem 1rem;
            transition: all var(--transition-fast);
            font-family: 'Inter', sans-serif;
        }}
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus {{
            border-color: var(--primary);
            outline: none;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}
        
        .stSlider > div > div > div > div {{
            color: var(--primary);
        }}
        
        /* ===== UPLOAD ZONE ===== */
        [data-testid="stFileUploader"] {{
            padding: 2rem;
            border: 2px dashed var(--card-border);
            border-radius: var(--radius-lg);
            background: var(--card-bg);
            transition: all var(--transition-base);
            cursor: pointer;
        }}
        
        [data-testid="stFileUploader"]:hover {{
            border-color: var(--primary);
            background: var(--input-bg);
            box-shadow: var(--shadow-md);
            transform: scale(1.01);
        }}
        
        [data-testid="stFileUploader"] > section > div {{
            padding: 1rem 0;
        }}
        
        /* ===== PROGRESS BAR ===== */
        .stProgress > div > div > div {{
            background: {primary_gradient};
            border-radius: var(--radius-full);
            box-shadow: var(--shadow-md);
        }}
        
        /* ===== ALERTS & MESSAGES ===== */
        .stAlert {{
            border-radius: var(--radius-lg);
            border-left: 4px solid var(--primary);
            padding: var(--space-lg);
            background: var(--card-bg);
            transition: all var(--transition-base);
        }}
        
        .stSuccess {{
            border-left-color: var(--success);
            background: rgba(16, 185, 129, 0.1);
        }}
        
        .stError {{
            border-left-color: var(--error);
            background: rgba(239, 68, 68, 0.1);
        }}
        
        .stWarning {{
            border-left-color: var(--warning);
            background: rgba(251, 191, 36, 0.1);
        }}
        
        .stInfo {{
            border-left-color: var(--primary);
            background: rgba(102, 126, 234, 0.1);
        }}
        
        /* ===== HEADER ===== */
        .header-container {{
            padding: var(--space-2xl) var(--space-md);
            text-align: center;
            position: relative;
            background: linear-gradient(135deg, transparent 0%, rgba(102, 126, 234, 0.05) 100%);
            border-radius: var(--radius-xl);
            margin-bottom: var(--space-xl);
        }}
        
        .header-title {{
            font-size: 3.5rem;
            font-weight: 800;
            background: {primary_gradient};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: var(--space-sm);
            animation: gradient-float 4s ease-in-out infinite;
            background-size: 200% 200%;
            letter-spacing: -0.02em;
        }}
        
        @keyframes gradient-float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-4px); }}
        }}
        
        .header-subtitle {{
            color: var(--text-secondary);
            font-size: 1.25rem;
            font-weight: 500;
            max-width: 600px;
            margin: 0 auto;
            line-height: 1.6;
        }}
        
        /* ===== THEME BADGE ===== */
        .theme-badge {{
            position: fixed;
            top: 1rem;
            right: 1rem;
            padding: var(--space-sm) var(--space-lg);
            background: var(--card-bg);
            border: 2px solid var(--card-border);
            border-radius: var(--radius-full);
            font-size: 1.25rem;
            cursor: pointer;
            transition: all var(--transition-base);
            z-index: 100;
            box-shadow: var(--shadow-md);
        }}
        
        .theme-badge:hover {{
            border-color: var(--primary);
            transform: scale(1.1);
            box-shadow: var(--shadow-lg);
        }}
        
        /* ===== SIDEBAR ===== */
        [data-testid="stSidebar"] {{
            background: var(--bg-secondary);
            border-right: 1px solid var(--border);
        }}
        
        /* ===== TABS ===== */
        .stTabs [data-baseweb="tab-list"] {{
            gap: var(--space-sm);
            border-bottom: 2px solid var(--card-border);
        }}
        
        .stTabs [data-baseweb="tab"] {{
            border-radius: var(--radius-md) var(--radius-md) 0 0;
            padding: var(--space-md) var(--space-lg);
            font-weight: 600;
            border: none;
            background: transparent;
            color: var(--text-secondary);
            transition: all var(--transition-base);
        }}
        
        .stTabs [data-baseweb="tab"][aria-selected="true"] {{
            color: var(--primary);
            border-bottom: 3px solid var(--primary);
            margin-bottom: -2px;
        }}
        
        /* ===== EXPANDER ===== */
        .streamlit-expanderHeader {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: var(--radius-lg);
            padding: var(--space-md);
            font-weight: 600;
            transition: all var(--transition-base);
        }}
        
        .streamlit-expanderHeader:hover {{
            border-color: var(--primary);
            box-shadow: var(--shadow-sm);
        }}
        
        /* ===== FOOTER ===== */
        .footer {{
            text-align: center;
            padding: var(--space-2xl) var(--space-lg);
            color: var(--text-secondary);
            font-size: 0.9rem;
            border-top: 1px solid var(--border);
            margin-top: var(--space-2xl);
        }}
        
        .footer-links {{
            display: flex;
            justify-content: center;
            gap: var(--space-xl);
            margin-top: var(--space-lg);
            flex-wrap: wrap;
        }}
        
        .footer-link {{
            color: var(--text-secondary);
            text-decoration: none;
            transition: color var(--transition-fast);
            font-weight: 500;
        }}
        
        .footer-link:hover {{
            color: var(--primary);
        }}
        
        /* ===== METRIC CARDS ===== */
        .metric-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: var(--space-lg);
            margin: var(--space-lg) 0;
        }}
        
        .metric-box {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: var(--radius-lg);
            padding: var(--space-lg);
            text-align: center;
            transition: all var(--transition-base);
            box-shadow: var(--shadow-sm);
        }}
        
        .metric-box:hover {{
            border-color: var(--primary);
            box-shadow: var(--shadow-md);
            transform: translateY(-2px);
        }}
        
        .metric-value {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary);
            line-height: 1;
        }}
        
        .metric-label {{
            font-size: 0.875rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: var(--space-sm);
            font-weight: 600;
        }}
        
        /* ===== BADGES ===== */
        .badge {{
            display: inline-block;
            padding: var(--space-xs) var(--space-md);
            border-radius: var(--radius-full);
            font-size: 0.75rem;
            font-weight: 700;
            background: var(--primary);
            color: white;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .badge.success {{
            background: var(--success);
        }}
        
        .badge.error {{
            background: var(--error);
        }}
        
        .badge.warning {{
            background: var(--warning);
            color: black;
        }}
        
        /* ===== SCROLLBAR ===== */
        ::-webkit-scrollbar {{
            width: 10px;
            height: 10px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: var(--bg-secondary);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: var(--card-border);
            border-radius: var(--radius-full);
            transition: background var(--transition-base);
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: var(--primary);
        }}
        
        /* ===== ANIMATIONS ===== */
        @keyframes slideIn {{
            from {{
                opacity: 0;
                transform: translateY(10px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        @keyframes fadeIn {{
            from {{
                opacity: 0;
            }}
            to {{
                opacity: 1;
            }}
        }}
        
        @keyframes pulse {{
            0%, 100% {{
                opacity: 1;
            }}
            50% {{
                opacity: 0.5;
            }}
        }}
        
        .fade-in {{
            animation: fadeIn var(--transition-base);
        }}
        
        .slide-in {{
            animation: slideIn var(--transition-base);
        }}
        
        .pulse {{
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }}
        
        /* ===== RESPONSIVE ===== */
        /* Tablet screens (768px - 1024px) */
        @media (max-width: 1024px) {{
            .stApp {{
                padding: 1rem;
            }}
            
            .header-container {{
                margin-bottom: 2rem;
            }}
            
            [data-testid="column"] {{
                padding: 0.5rem;
            }}
        }}
        
        /* Mobile screens (< 768px) */
        @media (max-width: 768px) {{
            /* Hide complex layouts on mobile */
            .stApp {{
                padding: 0.75rem;
            }}
            
            /* Typography adjustments */
            .header-title {{
                font-size: 1.75rem;
            }}
            
            .header-subtitle {{
                font-size: 0.9rem;
                margin-top: 0.5rem;
            }}
            
            h1 {{
                font-size: 1.75rem;
            }}
            
            h2 {{
                font-size: 1.3rem;
            }}
            
            h3 {{
                font-size: 1.1rem;
            }}
            
            /* Single column layout */
            .metric-row {{
                grid-template-columns: 1fr;
                gap: 0.75rem;
            }}
            
            /* Sidebar adjustments */
            [data-testid="stSidebar"] {{
                max-width: 100%;
            }}
            
            /* Button sizing for touch */
            button {{
                padding: 0.75rem 1rem;
                font-size: 1rem;
                min-height: 44px;
                border-radius: 8px;
            }}
            
            .stButton > button {{
                min-height: 48px;
                font-size: 1rem;
            }}
            
            /* Input sizing for touch */
            input, textarea, select {{
                min-height: 44px;
                font-size: 16px;
                padding: 0.75rem;
            }}
            
            /* Card adjustments */
            .stCard {{
                padding: 1rem;
                margin-bottom: 1rem;
            }}
            
            /* Tab adjustments */
            .stTabs {{
                margin-bottom: 1rem;
            }}
            
            [data-testid="stTab"] {{
                padding: 0.75rem;
            }}
            
            /* Comparison slider - touch-friendly */
            .comparison-slider {{
                height: auto;
                max-height: 400px;
            }}
            
            .comparison-slider-handle {{
                width: 6px;
            }}
            
            /* Result card grid - responsive */
            .results-grid {{
                grid-template-columns: 1fr;
            }}
            
            /* Footer adjustments */
            .footer {{
                padding: 1.5rem 1rem;
            }}
            
            .footer-links {{
                flex-direction: column;
                gap: 0.75rem;
            }}
            
            .footer-link {{
                font-size: 0.9rem;
            }}
            
            /* Alert and info boxes */
            [data-testid="stAlert"] {{
                padding: 0.75rem;
                margin: 0.75rem 0;
            }}
            
            /* Expandable sections */
            .stExpander {{
                margin-bottom: 0.75rem;
            }}
            
            /* Column spacing */
            [data-testid="column"] {{
                padding: 0.5rem !important;
                gap: 0.5rem;
            }}
            
            /* Image spacing */
            img {{
                max-width: 100%;
                height: auto;
            }}
            
            /* Reduce gaps in columns */
            .stColumns {{
                gap: 0.5rem;
            }}
        }}
        
        /* Extra small screens (< 480px) */
        @media (max-width: 480px) {{
            .header-title {{
                font-size: 1.5rem;
            }}
            
            .header-subtitle {{
                font-size: 0.85rem;
                line-height: 1.3;
            }}
            
            h1 {{
                font-size: 1.5rem;
            }}
            
            h2 {{
                font-size: 1.1rem;
            }}
            
            h3 {{
                font-size: 1rem;
            }}
            
            /* Extreme spacing reduction */
            .stApp {{
                padding: 0.5rem;
            }}
            
            .stCard {{
                padding: 0.75rem;
            }}
            
            .metric-row {{
                grid-template-columns: 1fr;
                gap: 0.5rem;
            }}
            
            /* Simplify footer on very small screens */
            .footer {{
                padding: 1rem 0.75rem;
                text-align: center;
            }}
            
            .footer-links {{
                justify-content: center;
            }}
            
            /* Compact buttons */
            button {{
                font-size: 0.95rem;
                padding: 0.6rem 0.8rem;
            }}
        }}
        </style>
    """, unsafe_allow_html=True)

def render_header(theme_mode="dark"):
    """Render the application header with theme toggle and indicator."""
    theme_icon = "●" if theme_mode == "dark" else "○"
    
    # Create two columns for header
    col1, col2 = st.columns([10, 1])
    
    with col1:
        st.markdown(f"""
            <div class="header-container">
                <div class="header-title">Depth Generator Pro</div>
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
            <div>Built with care using Depth Anything V2 • Streamlit • PyTorch</div>
            <div class="footer-links">
                <a href="https://github.com/DepthAnything/Depth-Anything-V2" class="footer-link" target="_blank">Documentation</a>
                <a href="https://github.com" class="footer-link" target="_blank">GitHub</a>
                <a href="#" class="footer-link">Settings</a>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_metric_card(label, value, icon=""):
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
