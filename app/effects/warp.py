"""Warp effect using noise field or wave."""
import numpy as np
import cv2
import random
import math
from typing import Dict, Any, Optional
from app.effects.base import Effect


class Warp(Effect):
    """Warp image using noise field or wave distortion."""
    
    name = "Warp"
    description = "Искажает изображение волнами или шумовым полем через обратное отображение."
    
    @classmethod
    def default_params(cls) -> Dict[str, Any]:
        return {
            "type": "wave",  # wave, noise
            "amount": 10.0,
            "scale": 50.0,
            "angle": 0.0,
            "seed": 42,
            "interpolation": "bicubic"  # nearest, bilinear, bicubic
        }
    
    @classmethod
    def apply(cls, image: np.ndarray, params: Dict[str, Any]) -> np.ndarray:
        warp_type = params.get("type", "wave")
        amount = float(params.get("amount", 10.0))
        scale = float(params.get("scale", 50.0))
        angle = float(params.get("angle", 0.0))
        seed = params.get("seed", 42)
        interpolation = params.get("interpolation", "bicubic")
        
        h, w = image.shape[:2]
        
        # Create coordinate maps
        map_x = np.zeros((h, w), dtype=np.float32)
        map_y = np.zeros((h, w), dtype=np.float32)
        
        # Generate base coordinates
        for y in range(h):
            for x in range(w):
                map_x[y, x] = x
                map_y[y, x] = y
        
        # Apply distortion
        if warp_type == "wave":
            cls._apply_wave(map_x, map_y, amount, scale, angle)
        elif warp_type == "noise":
            cls._apply_noise(map_x, map_y, amount, scale, seed)
        
        # Interpolation mapping
        interp_map = {
            "nearest": cv2.INTER_NEAREST,
            "bilinear": cv2.INTER_LINEAR,
            "bicubic": cv2.INTER_CUBIC
        }
        interp = interp_map.get(interpolation, cv2.INTER_CUBIC)
        
        # Apply remap (inverse mapping)
        result = cv2.remap(image, map_x, map_y, interp, borderMode=cv2.BORDER_REFLECT_101)
        
        return result
    
    @classmethod
    def _apply_wave(cls, map_x: np.ndarray, map_y: np.ndarray, 
                   amount: float, scale: float, angle: float):
        """Apply wave distortion."""
        h, w = map_x.shape
        angle_rad = math.radians(angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        for y in range(h):
            for x in range(w):
                # Rotate coordinates
                rx = x * cos_a - y * sin_a
                ry = x * sin_a + y * cos_a
                
                # Apply wave
                offset_x = amount * math.sin(ry / scale)
                offset_y = amount * math.cos(rx / scale)
                
                # Rotate back
                new_x = x + offset_x * cos_a - offset_y * sin_a
                new_y = y + offset_x * sin_a + offset_y * cos_a
                
                map_x[y, x] = max(0, min(w - 1, new_x))
                map_y[y, x] = max(0, min(h - 1, new_y))
    
    @classmethod
    def _apply_noise(cls, map_x: np.ndarray, map_y: np.ndarray,
                    amount: float, scale: float, seed: int):
        """Apply noise-like distortion using sinusoidal patterns."""
        h, w = map_x.shape
        random.seed(seed)
        
        # Generate multiple sine waves with random phases
        phases_x = [random.uniform(0, 2 * math.pi) for _ in range(3)]
        phases_y = [random.uniform(0, 2 * math.pi) for _ in range(3)]
        freqs_x = [random.uniform(0.5, 2.0) for _ in range(3)]
        freqs_y = [random.uniform(0.5, 2.0) for _ in range(3)]
        
        for y in range(h):
            for x in range(w):
                offset_x = 0
                offset_y = 0
                
                for i in range(3):
                    offset_x += amount * math.sin(x * freqs_x[i] / scale + phases_x[i]) / 3
                    offset_y += amount * math.sin(y * freqs_y[i] / scale + phases_y[i]) / 3
                
                new_x = x + offset_x
                new_y = y + offset_y
                
                map_x[y, x] = max(0, min(w - 1, new_x))
                map_y[y, x] = max(0, min(h - 1, new_y))
    
    @classmethod
    def randomize(cls, params: Dict[str, Any], seed: Optional[int] = None) -> Dict[str, Any]:
        import random
        if seed is not None:
            random.seed(seed)
        
        params = params.copy()
        params["type"] = random.choice(["wave", "noise"])
        params["amount"] = random.uniform(5.0, 30.0)
        params["scale"] = random.uniform(20.0, 100.0)
        params["angle"] = random.uniform(0, 360)
        params["seed"] = random.randint(0, 2**31 - 1)
        params["interpolation"] = random.choice(["bilinear", "bicubic"])
        return params
    
    @classmethod
    def get_intensity_param(cls) -> Optional[str]:
        return "amount"

