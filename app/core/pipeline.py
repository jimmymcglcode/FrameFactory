"""Effect pipeline for processing images."""
import numpy as np
from typing import List, Dict, Any, Optional, Callable
from copy import deepcopy


class EffectInstance:
    """Represents an effect instance in the pipeline."""
    
    def __init__(self, effect_class, params: Dict[str, Any], enabled: bool = True):
        self.effect_class = effect_class
        self.params = params
        self.enabled = enabled
        self.name = effect_class.name
    
    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply this effect instance."""
        if not self.enabled:
            return image
        return self.effect_class.apply(image, self.params)


class Pipeline:
    """Manages the effect pipeline."""
    
    def __init__(self):
        self.effects: List[EffectInstance] = []
        self.history: List[List[EffectInstance]] = []  # For undo/redo
        self.history_index: int = -1
        self.max_history = 50
    
    def add_effect(self, effect_class, params: Dict[str, Any]) -> EffectInstance:
        """Add an effect to the pipeline."""
        instance = EffectInstance(effect_class, params, enabled=True)
        self.effects.append(instance)
        self._save_state()
        return instance
    
    def remove_effect(self, index: int):
        """Remove effect at index."""
        if 0 <= index < len(self.effects):
            self.effects.pop(index)
            self._save_state()
    
    def set_effect_enabled(self, index: int, enabled: bool):
        """Enable/disable effect at index."""
        if 0 <= index < len(self.effects):
            self.effects[index].enabled = enabled
            self._save_state()
    
    def update_effect_params(self, index: int, params: Dict[str, Any]):
        """Update parameters of effect at index."""
        if 0 <= index < len(self.effects):
            self.effects[index].params = params
            self._save_state()
    
    def move_effect(self, from_index: int, to_index: int):
        """Move effect from one position to another."""
        if 0 <= from_index < len(self.effects) and 0 <= to_index < len(self.effects):
            effect = self.effects.pop(from_index)
            self.effects.insert(to_index, effect)
            self._save_state()
    
    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply all enabled effects in order."""
        result = image.copy()
        for effect in self.effects:
            if effect.enabled:
                try:
                    result = effect.apply(result)
                except Exception as e:
                    # If effect fails, continue with previous result
                    from app.core.logger import logger
                    logger.error(f"Error applying effect {effect.name}", e)
        return result
    
    def clear(self):
        """Clear all effects."""
        self.effects.clear()
        self._save_state()
    
    def get_effects(self) -> List[EffectInstance]:
        """Get list of effect instances."""
        return self.effects
    
    def _save_state(self):
        """Save current state to history for undo/redo."""
        # Deep copy current state
        state_copy = [EffectInstance(e.effect_class, deepcopy(e.params), e.enabled) 
                     for e in self.effects]
        
        # Remove future history if we're not at the end
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        
        self.history.append(state_copy)
        self.history_index += 1
        
        # Limit history size
        if len(self.history) > self.max_history:
            self.history.pop(0)
            self.history_index -= 1
    
    def undo(self) -> bool:
        """Undo last change. Returns True if undo was successful."""
        if self.history_index > 0:
            self.history_index -= 1
            self.effects = [EffectInstance(e.effect_class, deepcopy(e.params), e.enabled) 
                           for e in self.history[self.history_index]]
            return True
        return False
    
    def redo(self) -> bool:
        """Redo last undone change. Returns True if redo was successful."""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.effects = [EffectInstance(e.effect_class, deepcopy(e.params), e.enabled) 
                           for e in self.history[self.history_index]]
            return True
        return False
    
    def can_undo(self) -> bool:
        """Check if undo is possible."""
        return self.history_index > 0
    
    def can_redo(self) -> bool:
        """Check if redo is possible."""
        return self.history_index < len(self.history) - 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert pipeline to dictionary for preset saving."""
        return {
            "effects": [
                {
                    "class": effect.effect_class.__name__,
                    "params": effect.params,
                    "enabled": effect.enabled
                }
                for effect in self.effects
            ]
        }
    
    def from_dict(self, data: Dict[str, Any], effect_registry: Dict[str, Any]):
        """Load pipeline from dictionary."""
        self.effects.clear()
        for effect_data in data.get("effects", []):
            effect_class = effect_registry.get(effect_data["class"])
            if effect_class:
                instance = EffectInstance(
                    effect_class,
                    effect_data.get("params", {}),
                    effect_data.get("enabled", True)
                )
                self.effects.append(instance)
        
        # Reset history after loading preset
        self.history = []
        self.history_index = -1
        if self.effects:
            self._save_state()

