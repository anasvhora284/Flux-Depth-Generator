"""
Onboarding and welcome flow for first-time users.
Provides welcome modal, contextual tooltips, and progress indicators.
"""

import streamlit as st
from typing import Dict, List, Tuple
import json
from datetime import datetime
from pathlib import Path


def get_onboarding_state() -> Dict:
    """Get or initialize onboarding session state."""
    if 'onboarding_complete' not in st.session_state:
        st.session_state.onboarding_complete = False
    if 'show_welcome_modal' not in st.session_state:
        st.session_state.show_welcome_modal = should_show_welcome()
    if 'tooltips_enabled' not in st.session_state:
        st.session_state.tooltips_enabled = True
    if 'tooltip_history' not in st.session_state:
        st.session_state.tooltip_history = {}
    if 'progress_step' not in st.session_state:
        st.session_state.progress_step = 1
    
    return {
        'onboarding_complete': st.session_state.onboarding_complete,
        'show_welcome_modal': st.session_state.show_welcome_modal,
        'tooltips_enabled': st.session_state.tooltips_enabled,
        'tooltip_history': st.session_state.tooltip_history,
        'progress_step': st.session_state.progress_step,
    }


def should_show_welcome() -> bool:
    """Check if user is visiting for the first time."""
    onboarding_file = Path('.streamlit/onboarding.json')
    if onboarding_file.exists():
        try:
            with open(onboarding_file, 'r') as f:
                data = json.load(f)
                return not data.get('has_visited', False)
        except:
            return True
    return True


def mark_first_visit_complete():
    """Mark that user has completed first visit."""
    onboarding_file = Path('.streamlit/onboarding.json')
    onboarding_file.parent.mkdir(exist_ok=True)
    
    data = {
        'has_visited': True,
        'first_visit_date': datetime.now().isoformat(),
        'onboarding_version': '1.0'
    }
    
    with open(onboarding_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    st.session_state.show_welcome_modal = False
    st.session_state.onboarding_complete = True


def render_welcome_modal():
    """Render the first-visit welcome modal with overview of features."""
    welcome_html = """
    <style>
        .welcome-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            animation: fadeIn 0.3s ease-in;
        }
        
        .welcome-content {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 24px;
            padding: 48px;
            max-width: 600px;
            width: 90%;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            color: white;
            animation: slideUp 0.4s ease-out;
        }
        
        .welcome-header {
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 16px;
            text-align: center;
        }
        
        .welcome-subtitle {
            font-size: 16px;
            opacity: 0.9;
            margin-bottom: 32px;
            text-align: center;
            line-height: 1.5;
        }
        
        .welcome-features {
            display: grid;
            gap: 20px;
            margin-bottom: 32px;
        }
        
        .feature-item {
            display: flex;
            gap: 16px;
            align-items: flex-start;
        }
        
        .feature-icon {
            font-size: 24px;
            min-width: 24px;
        }
        
        .feature-text {
            flex: 1;
        }
        
        .feature-title {
            font-weight: 600;
            font-size: 15px;
            margin-bottom: 4px;
        }
        
        .feature-desc {
            font-size: 13px;
            opacity: 0.85;
            line-height: 1.4;
        }
        
        .welcome-buttons {
            display: flex;
            gap: 12px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .welcome-btn {
            padding: 12px 28px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 14px;
            border: none;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .welcome-btn-primary {
            background: white;
            color: #667eea;
            flex: 1;
            min-width: 140px;
        }
        
        .welcome-btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        
        .welcome-btn-secondary {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: 2px solid rgba(255, 255, 255, 0.3);
        }
        
        .welcome-btn-secondary:hover {
            background: rgba(255, 255, 255, 0.3);
            border-color: white;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
    
    <div class="welcome-modal">
        <div class="welcome-content">
            <div class="welcome-header">👋 Welcome to Flux Depth Generator</div>
            <div class="welcome-subtitle">
                Transform your images into stunning depth maps with AI-powered precision
            </div>
            
            <div class="welcome-features">
                <div class="feature-item">
                    <div class="feature-icon">🖼️</div>
                    <div class="feature-text">
                        <div class="feature-title">Upload & Process</div>
                        <div class="feature-desc">Drag and drop your images or videos to generate depth maps instantly</div>
                    </div>
                </div>
                
                <div class="feature-item">
                    <div class="feature-icon">🎨</div>
                    <div class="feature-text">
                        <div class="feature-title">Visualize & Customize</div>
                        <div class="feature-desc">Choose from 10+ colormaps and adjust depth range for perfect results</div>
                    </div>
                </div>
                
                <div class="feature-item">
                    <div class="feature-icon">💾</div>
                    <div class="feature-text">
                        <div class="feature-title">Export Multiple Formats</div>
                        <div class="feature-desc">Save as PNG, TIFF, EXR, NPY, RAW and use in 3D software</div>
                    </div>
                </div>
                
                <div class="feature-item">
                    <div class="feature-icon">⚡</div>
                    <div class="feature-text">
                        <div class="feature-title">Batch Processing</div>
                        <div class="feature-desc">Process multiple images at once and compare results side-by-side</div>
                    </div>
                </div>
                
                <div class="feature-item">
                    <div class="feature-icon">🎯</div>
                    <div class="feature-text">
                        <div class="feature-title">Professional Output</div>
                        <div class="feature-desc">Get publication-ready depth maps with high precision and quality</div>
                    </div>
                </div>
            </div>
            
            <div class="welcome-buttons">
                <button class="welcome-btn welcome-btn-primary" onclick="document.location.hash='#get-started'">
                    Get Started
                </button>
                <button class="welcome-btn welcome-btn-secondary" onclick="document.location.hash='#skip'">
                    Skip Tour
                </button>
            </div>
        </div>
    </div>
    """
    
    st.markdown(welcome_html, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Get Started", key="welcome_start", use_container_width=True):
            mark_first_visit_complete()
            st.rerun()
    with col2:
        if st.button("Skip for Now", key="welcome_skip", use_container_width=True):
            mark_first_visit_complete()
            st.rerun()


def render_tooltip(
    content: str,
    icon: str = "ℹ️",
    position: str = "bottom",
    always_visible: bool = False
) -> None:
    """
    Render a contextual tooltip.
    
    Args:
        content: Tooltip text content
        icon: Icon to display (default info icon)
        position: Position relative to element (top, bottom, left, right)
        always_visible: If True, always show; if False, only on hover
    """
    tooltip_html = f"""
    <style>
        .tooltip-container {{
            position: relative;
            display: inline-block;
            width: fit-content;
        }}
        
        .tooltip-icon {{
            display: inline-block;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: rgba(102, 126, 234, 0.1);
            border: 2px solid #667eea;
            color: #667eea;
            font-size: 12px;
            line-height: 16px;
            text-align: center;
            cursor: help;
            transition: all 0.2s ease;
        }}
        
        .tooltip-icon:hover {{
            background: #667eea;
            color: white;
            transform: scale(1.1);
        }}
        
        .tooltip-text {{
            visibility: hidden;
            width: 240px;
            background-color: #2c3e50;
            color: white;
            text-align: left;
            border-radius: 8px;
            padding: 12px;
            position: absolute;
            z-index: 100;
            font-size: 13px;
            line-height: 1.5;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            opacity: 0;
            transition: opacity 0.3s ease;
            pointer-events: none;
            bottom: 125%;
            left: 50%;
            margin-left: -120px;
        }}
        
        .tooltip-text::after {{
            content: "";
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -5px;
            border-width: 5px;
            border-style: solid;
            border-color: #2c3e50 transparent transparent transparent;
        }}
        
        .tooltip-container:hover .tooltip-text,
        .tooltip-text.always-visible {{
            visibility: visible;
            opacity: 1;
        }}
    </style>
    
    <div class="tooltip-container">
        <span class="tooltip-icon">{icon}</span>
        <span class="tooltip-text {'always-visible' if always_visible else ''}">{content}</span>
    </div>
    """
    
    st.markdown(tooltip_html, unsafe_allow_html=True)


def render_progress_indicator(
    current_step: int,
    total_steps: int = 4,
    step_labels: List[str] = None
) -> None:
    """
    Render a progress indicator showing workflow steps.
    
    Args:
        current_step: Current step (1-indexed)
        total_steps: Total number of steps
        step_labels: Labels for each step
    """
    if step_labels is None:
        step_labels = ["Upload", "Configure", "Process", "Export"]
    
    progress_html = """
    <style>
        .progress-container {
            margin: 24px 0;
        }
        
        .progress-steps {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
        }
        
        .progress-step {
            flex: 1;
        }
        
        .step-circle {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 14px;
            transition: all 0.3s ease;
            margin-bottom: 8px;
        }
        
        .step-circle.active {
            background: #667eea;
            color: white;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        
        .step-circle.completed {
            background: #10b981;
            color: white;
        }
        
        .step-circle.pending {
            background: #e5e7eb;
            color: #9ca3af;
        }
        
        .step-label {
            font-size: 12px;
            font-weight: 500;
            text-align: center;
            color: #6b7280;
        }
        
        .step-label.active {
            color: #667eea;
            font-weight: 600;
        }
        
        .step-label.completed {
            color: #10b981;
        }
        
        .progress-bar {
            height: 4px;
            background: #e5e7eb;
            border-radius: 2px;
            margin: 0 4px;
            flex: 1;
        }
        
        .progress-bar.filled {
            background: linear-gradient(90deg, #667eea, #764ba2);
        }
    </style>
    """
    
    st.markdown(progress_html, unsafe_allow_html=True)
    
    # Build progress visualization
    cols = st.columns([1, 0.3] * total_steps - 1 + [1])
    
    col_idx = 0
    for i in range(1, total_steps + 1):
        with cols[col_idx]:
            if i < current_step:
                status = "completed"
                symbol = "✓"
            elif i == current_step:
                status = "active"
                symbol = str(i)
            else:
                status = "pending"
                symbol = str(i)
            
            st.markdown(
                f'<div class="step-circle {status}">{symbol}</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="step-label {status}">{step_labels[i-1]}</div>',
                unsafe_allow_html=True
            )
        
        # Progress bar between steps
        if i < total_steps:
            col_idx += 1
            with cols[col_idx]:
                filled = "filled" if i < current_step else ""
                st.markdown(
                    f'<div class="progress-bar {filled}"></div>',
                    unsafe_allow_html=True
                )
        
        col_idx += 1


def render_quick_tip(
    tip: str,
    tip_type: str = "info",
    icon: str = "💡"
) -> None:
    """
    Render a quick tip/hint box.
    
    Args:
        tip: Tip text
        tip_type: Type of tip (info, success, warning, error)
        icon: Icon to display
    """
    colors = {
        "info": ("#667eea", "rgba(102, 126, 234, 0.1)"),
        "success": ("#10b981", "rgba(16, 185, 129, 0.1)"),
        "warning": ("#f59e0b", "rgba(245, 158, 11, 0.1)"),
        "error": ("#ef4444", "rgba(239, 68, 68, 0.1)"),
    }
    
    color, bg = colors.get(tip_type, colors["info"])
    
    tip_html = f"""
    <div style="
        background: {bg};
        border-left: 4px solid {color};
        padding: 12px 16px;
        border-radius: 6px;
        margin: 12px 0;
        font-size: 14px;
        color: #2c3e50;
        line-height: 1.5;
    ">
        <strong>{icon} {tip}</strong>
    </div>
    """
    
    st.markdown(tip_html, unsafe_allow_html=True)


def get_context_help(section: str) -> str:
    """Get contextual help text for different app sections."""
    help_texts = {
        "upload": "Drag and drop images or click to browse. Supports JPG, PNG, WebP, TIFF formats. Max 100MB per file.",
        "depth_model": "Depth Anything V2 uses advanced vision transformers trained on diverse datasets for accurate depth estimation.",
        "colormap": "Choose a colormap to visualize depth. Viridis is perceptually uniform; Jet has high contrast.",
        "depth_range": "Adjust the min/max depth values to focus on specific depth regions. Auto-detection uses image statistics.",
        "batch_processing": "Enable batch mode to process multiple images at once. Results are saved in timestamped folders.",
        "export_format": "Choose output format: PNG for web, TIFF/EXR for professional work, NPY/RAW for analysis.",
        "advanced_options": "Fine-tune processing parameters for specific use cases or artistic effects.",
    }
    return help_texts.get(section, "")


def render_feature_highlight(
    feature_name: str,
    description: str,
    icon: str = "✨",
    show_arrow: bool = True
) -> None:
    """
    Render a feature highlight box to call attention to new/important features.
    
    Args:
        feature_name: Name of the feature
        description: Description of the feature
        icon: Icon for the feature
        show_arrow: Whether to show a pointing arrow
    """
    highlight_html = f"""
    <div style="
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        border: 2px solid #667eea;
        border-radius: 12px;
        padding: 16px;
        margin: 16px 0;
        position: relative;
    ">
        <div style="font-size: 18px; margin-bottom: 8px;">
            <strong>{icon} {feature_name}</strong>
        </div>
        <div style="font-size: 14px; color: #4b5563; line-height: 1.5;">
            {description}
        </div>
        {f'<div style="position: absolute; top: -12px; right: 16px; font-size: 20px;">👉</div>' if show_arrow else ''}
    </div>
    """
    st.markdown(highlight_html, unsafe_allow_html=True)


def disable_tooltips():
    """Disable all tooltips in the session."""
    st.session_state.tooltips_enabled = False


def enable_tooltips():
    """Enable all tooltips in the session."""
    st.session_state.tooltips_enabled = True
