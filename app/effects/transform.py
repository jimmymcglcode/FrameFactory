"""Basic transforms: rotate, flip, crop, scale."""
import numpy as np
from typing import Dict, Any, Optional
from app.effects.base import Effect


class RotateFlip(Effect):
    """Rotate and/or flip image."""
    
    name = "Rotate/Flip"
    description = "Поворачивает и/или отражает изображение."
    
    @classmethod
    def default_params(cls) -> Dict[str, Any]:
        return {
            "rotation": 0,  # 0, 90, 180, 270
            "flip_horizontal": False,
            "flip_vertical": False
        }
    
    @classmethod
    def apply(cls, image: np.ndarray, params: Dict[str, Any]) -> np.ndarray:
        rotation = params.get("rotation", 0)
        flip_h = params.get("flip_horizontal", False)
        flip_v = params.get("flip_vertical", False)
        
        result = image.copy()
        
        # Rotate
        if rotation != 0:
            k = rotation // 90
            result = np.rot90(result, k)
        
        # Flip
        if flip_h:
            result = np.flip(result, axis=1)
        if flip_v:
            result = np.flip(result, axis=0)
        
        return result
    
    @classmethod
    def randomize(cls, params: Dict[str, Any], seed: Optional[int] = None) -> Dict[str, Any]:
        import random
        if seed is not None:
            random.seed(seed)
        
        params = params.copy()
        params["rotation"] = random.choice([0, 90, 180, 270])
        params["flip_horizontal"] = random.random() < 0.3
        params["flip_vertical"] = random.random() < 0.3
        return params


class Crop(Effect):
    """Crop image."""
    
    name = "Crop"
    description = "Обрезает изображение по заданным координатам."
    
    @classmethod
    def default_params(cls) -> Dict[str, Any]:
        return {
            "x": 0,
            "y": 0,
            "width": 100,  # Percentage or absolute
            "height": 100,
            "mode": "percent"  # percent, absolute
        }
    
    @classmethod
    def apply(cls, image: np.ndarray, params: Dict[str, Any]) -> np.ndarray:
        h, w = image.shape[:2]
        mode = params.get("mode", "percent")
        
        if mode == "percent":
            x = int(w * params.get("x", 0) / 100)
            y = int(h * params.get("y", 0) / 100)
            width = int(w * params.get("width", 100) / 100)
            height = int(h * params.get("height", 100) / 100)
        else:
            x = int(params.get("x", 0))
            y = int(params.get("y", 0))
            width = int(params.get("width", w))
            height = int(params.get("height", h))
        
        x = max(0, min(x, w - 1))
        y = max(0, min(y, h - 1))
        width = max(1, min(width, w - x))
        height = max(1, min(height, h - y))
        
        return image[y:y+height, x:x+width]
    
    @classmethod
    def randomize(cls, params: Dict[str, Any], seed: Optional[int] = None) -> Dict[str, Any]:
        import random
        if seed is not None:
            random.seed(seed)
        
        params = params.copy()
        params["x"] = random.randint(0, 20)
        params["y"] = random.randint(0, 20)
        params["width"] = random.randint(80, 100)
        params["height"] = random.randint(80, 100)
        return params


class Scale(Effect):
    """Scale image."""
    
    name = "Scale"
    description = "Изменяет размер изображения."
    
    @classmethod
    def default_params(cls) -> Dict[str, Any]:
        return {
            "scale_x": 100,  # Percentage
            "scale_y": 100,
            "interpolation": "lanczos"  # nearest, bilinear, bicubic, lanczos
        }
    
    @classmethod
    def apply(cls, image: np.ndarray, params: Dict[str, Any]) -> np.ndarray:
        from PIL import Image
        
        scale_x = params.get("scale_x", 100) / 100.0
        scale_y = params.get("scale_y", 100) / 100.0
        interpolation = params.get("interpolation", "lanczos")
        
        h, w = image.shape[:2]
        new_w = int(w * scale_x)
        new_h = int(h * scale_y)
        
        interp_map = {
            "nearest": Image.Resampling.NEAREST,
            "bilinear": Image.Resampling.BILINEAR,
            "bicubic": Image.Resampling.BICUBIC,
            "lanczos": Image.Resampling.LANCZOS
        }
        interp = interp_map.get(interpolation, Image.Resampling.LANCZOS)
        
        pil_image = Image.fromarray(image)
        pil_image = pil_image.resize((new_w, new_h), interp)
        
        return np.array(pil_image, dtype=np.uint8)
    
    @classmethod
    def randomize(cls, params: Dict[str, Any], seed: Optional[int] = None) -> Dict[str, Any]:
        import random
        if seed is not None:
            random.seed(seed)
        
        params = params.copy()
        scale = random.uniform(80, 120)
        params["scale_x"] = scale
        params["scale_y"] = scale
        params["interpolation"] = random.choice(["bilinear", "bicubic", "lanczos"])
        return params

