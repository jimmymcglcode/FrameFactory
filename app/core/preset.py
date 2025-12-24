"""Preset save/load functionality."""
import json
import random
from typing import Dict, Any, List, Optional
from pathlib import Path


class PresetManager:
    """Manages saving and loading presets."""
    
    def __init__(self, effect_registry: Dict[str, Any]):
        self.effect_registry = effect_registry
    
    def save_preset(self, pipeline_data: Dict[str, Any], filepath: str) -> bool:
        """Save pipeline as preset to JSON file."""
        try:
            preset_data = {
                "version": "1.0",
                "pipeline": pipeline_data,
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(preset_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            from app.core.logger import logger
            logger.error(f"Failed to save preset to {filepath}", e)
            return False
    
    def load_preset(self, filepath: str) -> Optional[Dict[str, Any]]:
        """Load preset from JSON file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                preset_data = json.load(f)
            
            # Support both old format (direct pipeline) and new format (with version)
            if "pipeline" in preset_data:
                return preset_data["pipeline"]
            return preset_data
        except Exception as e:
            from app.core.logger import logger
            logger.error(f"Failed to load preset from {filepath}", e)
            return None
    
    def generate_random_preset(self, num_effects: int = None) -> Dict[str, Any]:
        """Generate random preset with 1-3 effects."""
        if num_effects is None:
            num_effects = random.randint(1, 3)
        
        available_effects = list(self.effect_registry.values())
        selected_effects = random.sample(available_effects, min(num_effects, len(available_effects)))
        
        effects_data = []
        for effect_class in selected_effects:
            # Get default params and randomize them
            params = effect_class.default_params()
            if hasattr(effect_class, 'randomize'):
                params = effect_class.randomize(params, seed=random.randint(0, 2**31 - 1))
            
            effects_data.append({
                "class": effect_class.__name__,
                "params": params,
                "enabled": True
            })
        
        return {
            "effects": effects_data
        }

