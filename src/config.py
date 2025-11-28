"""Configuration and settings management for persistent user preferences."""
import json
import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".depth_generator"
CONFIG_FILE = CONFIG_DIR / "settings.json"

DEFAULT_SETTINGS = {
    "theme": "auto",  # auto, light, dark
    "model_type": "vits",
    "accent_color": "#238636",
    "colormap": "grayscale",  # grayscale, viridis, plasma, inferno, turbo, jet
    "show_metrics": True,
    "show_live_preview": True,
    "output_format": "both",  # both, depth_only, 3d_only
    "depth_format": "png",  # png, tiff, exr
    "jpeg_quality": 95,
    "auto_download": False,
    "user_theme_preference": None,  # None, light, dark (user's explicit choice)
}

def load_settings():
    """Load user settings from disk."""
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r') as f:
                loaded = json.load(f)
                # Merge with defaults to handle new settings
                return {**DEFAULT_SETTINGS, **loaded}
    except Exception:
        pass
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    """Save user settings to disk."""
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
        return True
    except Exception:
        return False

def get_theme_colors(theme_mode):
    """Get color palette based on theme."""
    if theme_mode == "light":
        return {
            "bg_primary": "#ffffff",
            "bg_secondary": "#f6f8fa",
            "bg_tertiary": "#ffffff",
            "text_primary": "#24292f",
            "text_secondary": "#57606a",
            "border": "#d0d7de",
            "accent": "#0969da",
            "success": "#1a7f37",
            "warning": "#9a6700",
            "error": "#cf222e",
            "card_bg": "#ffffff",
            "card_border": "#d0d7de",
            "input_bg": "#f6f8fa",
        }
    else:  # dark
        return {
            "bg_primary": "#0d1117",
            "bg_secondary": "#161b22",
            "bg_tertiary": "#0d1117",
            "text_primary": "#e6edf3",
            "text_secondary": "#7d8590",
            "border": "#30363d",
            "accent": "#2f81f7",
            "success": "#238636",
            "warning": "#e3b341",
            "error": "#f85149",
            "card_bg": "#161b22",
            "card_border": "#30363d",
            "input_bg": "#0d1117",
        }

COLORMAPS = {
    "grayscale": "Grayscale",
    "viridis": "Viridis",
    "plasma": "Plasma",
    "inferno": "Inferno",
    "turbo": "Turbo",
    "jet": "Jet",
    "ocean": "Ocean",
    "rainbow": "Rainbow",
}

def get_system_theme():
    """Detect system dark mode preference (CSS prefers-color-scheme)."""
    import platform
    system = platform.system()
    
    try:
        if system == "Darwin":  # macOS
            import subprocess
            result = subprocess.run(
                ["defaults", "read", "-g", "AppleInterfaceStyle"],
                capture_output=True,
                text=True
            )
            return "dark" if "Dark" in result.stdout else "light"
        elif system == "Windows":
            import winreg
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
                value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                return "light" if value == 1 else "dark"
            except:
                return "dark"
        elif system == "Linux":
            # Check common desktop environments
            env = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
            # Most Linux systems default to light, we'll return light unless we detect dark explicitly
            return "light"
    except:
        pass
    
    return "light"  # Default fallback

def resolve_theme(settings):
    """Resolve the final theme to use based on settings and system preference."""
    if settings.get("user_theme_preference"):
        return settings["user_theme_preference"]
    
    if settings.get("theme") == "auto":
        return get_system_theme()
    
    return settings.get("theme", "dark")

