"""Grain and sharpen/blur effects."""
import numpy as np
import cv2
import random
from typing import Dict, Any, Optional
from app.effects.base import Effect


class Grain(Effect):
    """Add film grain noise."""
    
    name = "Grain"
    description = "Добавляет зернистость (шум) к изображению."
    
    @classmethod
    def default_params(cls) -> Dict[str, Any]:
        return {
            "amount": 0.3,  # 0 to 1
            "size": 2,  # 1 to 5
            "monochrome": False
        }
    
    @classmethod
    def apply(cls, image: np.ndarray, params: Dict[str, Any]) -> np.ndarray:
        amount = params.get("amount", 0.3)
        size = int(params.get("size", 2))
        monochrome = params.get("monochrome", False)
        
        h, w = image.shape[:2]
        
        # Generate noise
        if monochrome:
            # Single channel noise
            noise = np.random.normal(0, 1, (h, w))
        else:
            # Per-channel noise
            noise = np.random.normal(0, 1, (h, w, 3))
        
        # Scale noise
        noise_intensity = amount * 50  # Scale to pixel values
        noise = noise * noise_intensity
        
        # Apply size (blur the noise slightly)
        if size > 1:
            kernel_size = size * 2 + 1
            if monochrome:
                noise = cv2.GaussianBlur(noise, (kernel_size, kernel_size), 0)
            else:
                for c in range(3):
                    noise[:, :, c] = cv2.GaussianBlur(noise[:, :, c], (kernel_size, kernel_size), 0)
        
        # Add noise to image
        result = image.astype(np.float32) + noise
        result = np.clip(result, 0, 255).astype(np.uint8)
        
        return result
    
    @classmethod
    def randomize(cls, params: Dict[str, Any], seed: Optional[int] = None) -> Dict[str, Any]:
        import random
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        
        params = params.copy()
        params["amount"] = random.uniform(0.1, 0.5)
        params["size"] = random.randint(1, 4)
        params["monochrome"] = random.random() < 0.3
        return params
    
    @classmethod
    def get_intensity_param(cls) -> Optional[str]:
        return "amount"


class SharpenBlur(Effect):
    """Sharpen or blur image."""
    
    name = "Sharpen/Blur"
    description = "Увеличивает резкость или размывает изображение."
    
    @classmethod
    def default_params(cls) -> Dict[str, Any]:
        return {
            "mode": "blur",  # blur, sharpen
            "blur_sigma": 2.0,  # 0 to 10 (for blur)
            "sharpen_amount": 1.0  # 0 to 2 (for sharpen)
        }
    
    @classmethod
    def apply(cls, image: np.ndarray, params: Dict[str, Any]) -> np.ndarray:
        mode = params.get("mode", "blur")
        
        if mode == "blur":
            sigma = params.get("blur_sigma", 2.0)
            kernel_size = int(sigma * 6) | 1  # Make odd
            kernel_size = max(3, min(kernel_size, 51))
            
            result = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
        elif mode == "sharpen":
            amount = params.get("sharpen_amount", 1.0)
            # Unsharp mask: original + (original - blurred) * amount
            blurred = cv2.GaussianBlur(image, (5, 5), 1.0)
            result = image.astype(np.float32) + (image.astype(np.float32) - blurred.astype(np.float32)) * amount
            result = np.clip(result, 0, 255).astype(np.uint8)
        else:
            result = image.copy()
        
        return result
    
    @classmethod
    def randomize(cls, params: Dict[str, Any], seed: Optional[int] = None) -> Dict[str, Any]:
        import random
        if seed is not None:
            random.seed(seed)
        
        params = params.copy()
        params["mode"] = random.choice(["blur", "sharpen"])
        params["blur_sigma"] = random.uniform(1.0, 5.0)
        params["sharpen_amount"] = random.uniform(0.5, 1.5)
        return params
    
    @classmethod
    def get_intensity_param(cls) -> Optional[str]:
        return "blur_sigma"

