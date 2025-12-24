"""Base class for image effects."""
import numpy as np
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class Effect(ABC):
    """Base class for all image effects."""
    
    name: str = "Base Effect"
    description: str = "Base effect class"
    
    @classmethod
    @abstractmethod
    def default_params(cls) -> Dict[str, Any]:
        """Return default parameters for this effect."""
        pass
    
    @classmethod
    @abstractmethod
    def apply(cls, image: np.ndarray, params: Dict[str, Any]) -> np.ndarray:
        """Apply effect to image. Returns new image array."""
        pass
    
    @classmethod
    def randomize(cls, params: Dict[str, Any], seed: Optional[int] = None) -> Dict[str, Any]:
        """Randomize parameters within safe ranges."""
        import random
        if seed is not None:
            random.seed(seed)
        return params
    
    @classmethod
    def get_intensity_param(cls) -> Optional[str]:
        """Return name of intensity parameter, if any."""
        return None

