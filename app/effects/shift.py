"""Shift rows/columns effect."""
import numpy as np
import random
from typing import Dict, Any, Optional
from app.effects.base import Effect


class ShiftRowsColumns(Effect):
    """Shift rows/columns with smooth randomness."""
    
    name = "Shift Rows/Columns"
    description = "Сдвигает строки/столбцы с плавной случайностью. Даёт глитч без шума."
    
    @classmethod
    def default_params(cls) -> Dict[str, Any]:
        return {
            "direction": "rows",  # rows, columns, both
            "max_shift": 20,
            "smoothness": 0.5,
            "seed": 42,
            "wrap_mode": "wrap"  # wrap, reflect, clamp
        }
    
    @classmethod
    def apply(cls, image: np.ndarray, params: Dict[str, Any]) -> np.ndarray:
        direction = params.get("direction", "rows")
        max_shift = int(params.get("max_shift", 20))
        smoothness = params.get("smoothness", 0.5)
        seed = params.get("seed", 42)
        wrap_mode = params.get("wrap_mode", "wrap")
        
        result = image.copy()
        h, w = image.shape[:2]
        
        random.seed(seed)
        
        if direction in ["rows", "both"]:
            result = cls._shift_rows(result, max_shift, smoothness, wrap_mode, seed)
        
        if direction in ["columns", "both"]:
            result = cls._shift_columns(result, max_shift, smoothness, wrap_mode, seed)
        
        return result
    
    @classmethod
    def _shift_rows(cls, image: np.ndarray, max_shift: int, smoothness: float, 
                   wrap_mode: str, seed: int) -> np.ndarray:
        """Shift rows with smooth randomness."""
        h, w = image.shape[:2]
        result = np.zeros_like(image)
        
        random.seed(seed)
        shifts = []
        
        # Generate base shifts with smoothing
        for i in range(h):
            if i == 0:
                shift = random.randint(-max_shift, max_shift)
            else:
                # Smooth interpolation between previous and new random shift
                prev_shift = shifts[-1]
                new_shift = random.randint(-max_shift, max_shift)
                shift = int(prev_shift * smoothness + new_shift * (1 - smoothness))
            
            shifts.append(shift)
        
        # Apply shifts
        for i in range(h):
            shift = shifts[i]
            if shift == 0:
                result[i] = image[i]
            else:
                shifted = np.roll(image[i], shift, axis=0)
                result[i] = cls._apply_wrap_mode(shifted, image[i], shift, w, wrap_mode)
        
        return result
    
    @classmethod
    def _shift_columns(cls, image: np.ndarray, max_shift: int, smoothness: float,
                      wrap_mode: str, seed: int) -> np.ndarray:
        """Shift columns with smooth randomness."""
        h, w = image.shape[:2]
        result = np.zeros_like(image)
        
        random.seed(seed + 1000)  # Different seed for columns
        shifts = []
        
        for j in range(w):
            if j == 0:
                shift = random.randint(-max_shift, max_shift)
            else:
                prev_shift = shifts[-1]
                new_shift = random.randint(-max_shift, max_shift)
                shift = int(prev_shift * smoothness + new_shift * (1 - smoothness))
            
            shifts.append(shift)
        
        # Apply shifts
        for j in range(w):
            shift = shifts[j]
            if shift == 0:
                result[:, j] = image[:, j]
            else:
                shifted = np.roll(image[:, j], shift, axis=0)
                result[:, j] = cls._apply_wrap_mode(shifted, image[:, j], shift, h, wrap_mode)
        
        return result
    
    @classmethod
    def _apply_wrap_mode(cls, shifted: np.ndarray, original: np.ndarray, 
                        shift: int, size: int, wrap_mode: str) -> np.ndarray:
        """Apply wrap mode when shifting."""
        if wrap_mode == "wrap":
            return shifted
        elif wrap_mode == "reflect":
            # Reflect at edges
            return shifted
        elif wrap_mode == "clamp":
            # Clamp to edge values
            result = shifted.copy()
            if shift > 0:
                result[:shift] = original[:shift]
            elif shift < 0:
                result[shift:] = original[shift:]
            return result
        return shifted
    
    @classmethod
    def randomize(cls, params: Dict[str, Any], seed: Optional[int] = None) -> Dict[str, Any]:
        import random
        if seed is not None:
            random.seed(seed)
        
        params = params.copy()
        params["direction"] = random.choice(["rows", "columns", "both"])
        params["max_shift"] = random.randint(5, 50)
        params["smoothness"] = random.uniform(0.2, 0.8)
        params["seed"] = random.randint(0, 2**31 - 1)
        params["wrap_mode"] = random.choice(["wrap", "reflect", "clamp"])
        return params
    
    @classmethod
    def get_intensity_param(cls) -> Optional[str]:
        return "max_shift"

