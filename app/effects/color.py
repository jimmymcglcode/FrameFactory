"""Color effects: HSV, RGB curves, channel shuffle, posterize."""
import numpy as np
import cv2
from typing import Dict, Any, Optional
from app.effects.base import Effect


class HSVAdjust(Effect):
    """HSV/HSL adjustments."""
    
    name = "HSV Adjust"
    description = "Корректирует оттенок, насыщенность и яркость."
    
    @classmethod
    def default_params(cls) -> Dict[str, Any]:
        return {
            "hue_shift": 0,  # -180 to 180
            "saturation": 1.0,  # 0 to 2
            "value": 1.0  # 0 to 2 (brightness)
        }
    
    @classmethod
    def apply(cls, image: np.ndarray, params: Dict[str, Any]) -> np.ndarray:
        hue_shift = params.get("hue_shift", 0)
        saturation = params.get("saturation", 1.0)
        value = params.get("value", 1.0)
        
        # Convert RGB to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV).astype(np.float32)
        
        # Adjust hue (0-179 range in OpenCV)
        hsv[:, :, 0] = (hsv[:, :, 0] + hue_shift) % 180
        
        # Adjust saturation
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation, 0, 255)
        
        # Adjust value/brightness
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * value, 0, 255)
        
        # Convert back to RGB
        hsv = hsv.astype(np.uint8)
        result = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        
        return result
    
    @classmethod
    def randomize(cls, params: Dict[str, Any], seed: Optional[int] = None) -> Dict[str, Any]:
        import random
        if seed is not None:
            random.seed(seed)
        
        params = params.copy()
        params["hue_shift"] = random.randint(-60, 60)
        params["saturation"] = random.uniform(0.5, 1.5)
        params["value"] = random.uniform(0.7, 1.3)
        return params
    
    @classmethod
    def get_intensity_param(cls) -> Optional[str]:
        return "saturation"


class RGBCurves(Effect):
    """RGB curves: contrast, gamma, exposure."""
    
    name = "RGB Curves"
    description = "Корректирует контраст, гамму и экспозицию."
    
    @classmethod
    def default_params(cls) -> Dict[str, Any]:
        return {
            "contrast": 0,  # -100 to 100
            "gamma": 1.0,  # 0.2 to 3.0
            "exposure": 0.0  # -2 to 2
        }
    
    @classmethod
    def apply(cls, image: np.ndarray, params: Dict[str, Any]) -> np.ndarray:
        contrast = params.get("contrast", 0)
        gamma = params.get("gamma", 1.0)
        exposure = params.get("exposure", 0.0)
        
        result = image.astype(np.float32) / 255.0
        
        # Contrast adjustment
        if contrast != 0:
            factor = (259.0 * (contrast + 255)) / (255.0 * (259 - contrast))
            result = np.clip(factor * (result - 0.5) + 0.5, 0, 1)
        
        # Gamma correction
        if gamma != 1.0:
            result = np.power(result, 1.0 / gamma)
        
        # Exposure adjustment
        if exposure != 0.0:
            result = result * (2.0 ** exposure)
        
        result = np.clip(result * 255.0, 0, 255).astype(np.uint8)
        
        return result
    
    @classmethod
    def randomize(cls, params: Dict[str, Any], seed: Optional[int] = None) -> Dict[str, Any]:
        import random
        if seed is not None:
            random.seed(seed)
        
        params = params.copy()
        params["contrast"] = random.randint(-30, 30)
        params["gamma"] = random.uniform(0.8, 1.2)
        params["exposure"] = random.uniform(-0.5, 0.5)
        return params
    
    @classmethod
    def get_intensity_param(cls) -> Optional[str]:
        return "contrast"


class ChannelShuffle(Effect):
    """Channel shuffle and mixing."""
    
    name = "Channel Shuffle"
    description = "Переставляет каналы RGB и смешивает их."
    
    @classmethod
    def default_params(cls) -> Dict[str, Any]:
        return {
            "mode": "rgb",  # rgb, rbg, grb, gbr, brg, bgr, mix
            "mix_amount": 0.3  # 0 to 1 (only for mix mode)
        }
    
    @classmethod
    def apply(cls, image: np.ndarray, params: Dict[str, Any]) -> np.ndarray:
        mode = params.get("mode", "rgb")
        mix_amount = params.get("mix_amount", 0.3)
        
        r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]
        
        if mode == "rgb":
            result = np.stack([r, g, b], axis=2)
        elif mode == "rbg":
            result = np.stack([r, b, g], axis=2)
        elif mode == "grb":
            result = np.stack([g, r, b], axis=2)
        elif mode == "gbr":
            result = np.stack([g, b, r], axis=2)
        elif mode == "brg":
            result = np.stack([b, r, g], axis=2)
        elif mode == "bgr":
            result = np.stack([b, g, r], axis=2)
        elif mode == "mix":
            # Mix channels: blend R with G, G with B, B with R
            result = np.stack([
                (r * (1 - mix_amount) + g * mix_amount).astype(np.uint8),
                (g * (1 - mix_amount) + b * mix_amount).astype(np.uint8),
                (b * (1 - mix_amount) + r * mix_amount).astype(np.uint8)
            ], axis=2)
        else:
            result = image.copy()
        
        return result
    
    @classmethod
    def randomize(cls, params: Dict[str, Any], seed: Optional[int] = None) -> Dict[str, Any]:
        import random
        if seed is not None:
            random.seed(seed)
        
        params = params.copy()
        params["mode"] = random.choice(["rgb", "rbg", "grb", "gbr", "brg", "bgr", "mix"])
        params["mix_amount"] = random.uniform(0.2, 0.5)
        return params


class Posterize(Effect):
    """Color quantization / posterization."""
    
    name = "Posterize"
    description = "Уменьшает количество цветов (постеризация)."
    
    @classmethod
    def default_params(cls) -> Dict[str, Any]:
        return {
            "levels": 8,  # 2 to 256
            "dither": False
        }
    
    @classmethod
    def apply(cls, image: np.ndarray, params: Dict[str, Any]) -> np.ndarray:
        levels = int(params.get("levels", 8))
        dither = params.get("dither", False)
        
        levels = max(2, min(256, levels))
        
        if dither:
            # Simple ordered dithering
            result = cls._ordered_dither(image, levels)
        else:
            # Simple quantization
            step = 256 // levels
            result = (image // step * step).astype(np.uint8)
        
        return result
    
    @classmethod
    def _ordered_dither(cls, image: np.ndarray, levels: int) -> np.ndarray:
        """Apply ordered dithering."""
        h, w = image.shape[:2]
        step = 256 // levels
        
        # Bayer matrix 4x4 for dithering
        bayer = np.array([
            [0, 8, 2, 10],
            [12, 4, 14, 6],
            [3, 11, 1, 9],
            [15, 7, 13, 5]
        ]) / 16.0
        
        result = image.copy().astype(np.float32)
        
        for y in range(h):
            for x in range(w):
                threshold = bayer[y % 4, x % 4]
                value = image[y, x].astype(np.float32)
                quantized = (value // step) * step
                
                if (value % step) / step > threshold:
                    quantized = min(255, quantized + step)
                
                result[y, x] = quantized
        
        return result.astype(np.uint8)
    
    @classmethod
    def randomize(cls, params: Dict[str, Any], seed: Optional[int] = None) -> Dict[str, Any]:
        import random
        if seed is not None:
            random.seed(seed)
        
        params = params.copy()
        params["levels"] = random.choice([4, 8, 16, 32, 64])
        params["dither"] = random.random() < 0.5
        return params
    
    @classmethod
    def get_intensity_param(cls) -> Optional[str]:
        return "levels"

