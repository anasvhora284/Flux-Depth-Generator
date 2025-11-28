"""History and presets management for the application."""

import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional


HISTORY_DIR = Path.home() / ".depth_generator" / "history"
PRESETS_FILE = Path.home() / ".depth_generator" / "presets.json"


@dataclass
class ProcessingPreset:
    """Preset for processing settings."""
    name: str
    colormap: str = "grayscale"
    invert_depth: bool = False
    near_distance: int = 0
    far_distance: int = 100
    output_formats: List[str] = None
    model_type: str = "vits"
    
    def __post_init__(self):
        if self.output_formats is None:
            self.output_formats = ["PNG (Depth Map)", "JPEG (3D)"]


@dataclass
class ProcessingHistory:
    """Record of a processed image."""
    filename: str
    timestamp: str
    model_type: str
    colormap: str
    dimensions: str  # "WxH"
    file_size_kb: float


class HistoryManager:
    """Manage processing history."""
    
    def __init__(self):
        """Initialize history manager."""
        HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    
    def add_record(self, history_item: ProcessingHistory):
        """Add a record to history.
        
        Args:
            history_item: ProcessingHistory object
        """
        history_file = HISTORY_DIR / f"history_{datetime.now().strftime('%Y%m%d')}.json"
        
        records = []
        if history_file.exists():
            with open(history_file, 'r') as f:
                records = json.load(f)
        
        records.append(asdict(history_item))
        
        with open(history_file, 'w') as f:
            json.dump(records, f, indent=2)
    
    def get_recent(self, days=7):
        """Get recent processing history.
        
        Args:
            days: Number of days to look back
        
        Returns:
            List of ProcessingHistory objects
        """
        all_records = []
        
        for history_file in HISTORY_DIR.glob("history_*.json"):
            try:
                with open(history_file, 'r') as f:
                    records = json.load(f)
                    all_records.extend(records)
            except:
                pass
        
        # Sort by timestamp, most recent first
        all_records.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return [ProcessingHistory(**r) for r in all_records[:50]]  # Return last 50
    
    def clear_history(self):
        """Clear all history."""
        for history_file in HISTORY_DIR.glob("history_*.json"):
            history_file.unlink()


class PresetsManager:
    """Manage processing presets."""
    
    def __init__(self):
        """Initialize presets manager."""
        PRESETS_FILE.parent.mkdir(parents=True, exist_ok=True)
        self._default_presets = [
            ProcessingPreset(
                name="Fast Processing",
                model_type="vits",
                colormap="grayscale"
            ),
            ProcessingPreset(
                name="Balanced Quality",
                model_type="vitb",
                colormap="viridis"
            ),
            ProcessingPreset(
                name="Maximum Quality",
                model_type="vitl",
                colormap="turbo",
                output_formats=["PNG (Depth Map)", "JPEG (3D)"]
            ),
            ProcessingPreset(
                name="Heat Map Visualization",
                model_type="vitb",
                colormap="heatmap"
            ),
            ProcessingPreset(
                name="Close-up Focus",
                model_type="vitb",
                near_distance=25,
                far_distance=75
            ),
        ]
        
        # Load or create presets
        if not PRESETS_FILE.exists():
            self.save_presets(self._default_presets)
    
    def get_presets(self) -> List[ProcessingPreset]:
        """Get all presets.
        
        Returns:
            List of ProcessingPreset objects
        """
        try:
            if PRESETS_FILE.exists():
                with open(PRESETS_FILE, 'r') as f:
                    data = json.load(f)
                    return [ProcessingPreset(**p) for p in data]
        except:
            pass
        
        return self._default_presets
    
    def get_preset(self, name: str) -> Optional[ProcessingPreset]:
        """Get a specific preset by name.
        
        Args:
            name: Preset name
        
        Returns:
            ProcessingPreset or None if not found
        """
        presets = self.get_presets()
        for preset in presets:
            if preset.name == name:
                return preset
        return None
    
    def save_preset(self, preset: ProcessingPreset):
        """Save or update a preset.
        
        Args:
            preset: ProcessingPreset object
        """
        presets = self.get_presets()
        
        # Replace if exists, otherwise add
        found = False
        for i, p in enumerate(presets):
            if p.name == preset.name:
                presets[i] = preset
                found = True
                break
        
        if not found:
            presets.append(preset)
        
        self.save_presets(presets)
    
    def save_presets(self, presets: List[ProcessingPreset]):
        """Save all presets.
        
        Args:
            presets: List of ProcessingPreset objects
        """
        with open(PRESETS_FILE, 'w') as f:
            json.dump([asdict(p) for p in presets], f, indent=2)
    
    def delete_preset(self, name: str) -> bool:
        """Delete a preset.
        
        Args:
            name: Preset name
        
        Returns:
            True if deleted, False if not found
        """
        presets = self.get_presets()
        original_len = len(presets)
        
        presets = [p for p in presets if p.name != name]
        
        if len(presets) < original_len:
            self.save_presets(presets)
            return True
        
        return False
    
    def get_preset_names(self) -> List[str]:
        """Get list of preset names.
        
        Returns:
            List of preset names
        """
        presets = self.get_presets()
        return [p.name for p in presets]
