"""Image model for storing original, preview, and result images."""
import numpy as np
from PIL import Image
from typing import Optional, Tuple


class ImageModel:
    """Manages original image, preview, and processed result."""
    
    MAX_PREVIEW_SIZE = 1024  # Max dimension for preview
    
    def __init__(self):
        self.original_image: Optional[np.ndarray] = None
        self.original_size: Optional[Tuple[int, int]] = None
        self.preview_image: Optional[np.ndarray] = None
        self.result_image: Optional[np.ndarray] = None
        self.image_format: Optional[str] = None
        self.filename: Optional[str] = None
    
    def load_image(self, filepath: str) -> bool:
        """Load image from file."""
        try:
            pil_image = Image.open(filepath)
            # Convert to RGB if necessary
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            
            self.original_image = np.array(pil_image, dtype=np.uint8)
            self.original_size = (self.original_image.shape[1], self.original_image.shape[0])
            self.image_format = pil_image.format or 'PNG'
            self.filename = filepath
            
            # Create preview
            self._create_preview()
            
            return True
        except Exception as e:
            return False
    
    def _create_preview(self):
        """Create downscaled preview for faster processing."""
        if self.original_image is None:
            return
        
        h, w = self.original_image.shape[:2]
        max_dim = max(h, w)
        
        if max_dim <= self.MAX_PREVIEW_SIZE:
            self.preview_image = self.original_image.copy()
        else:
            scale = self.MAX_PREVIEW_SIZE / max_dim
            new_w = int(w * scale)
            new_h = int(h * scale)
            
            from PIL import Image
            pil_preview = Image.fromarray(self.original_image)
            pil_preview = pil_preview.resize((new_w, new_h), Image.Resampling.LANCZOS)
            self.preview_image = np.array(pil_preview, dtype=np.uint8)
    
    def has_image(self) -> bool:
        """Check if image is loaded."""
        return self.original_image is not None
    
    def get_original(self) -> Optional[np.ndarray]:
        """Get original full-size image."""
        return self.original_image
    
    def get_preview(self) -> Optional[np.ndarray]:
        """Get preview image."""
        return self.preview_image
    
    def set_result(self, image: np.ndarray, is_preview: bool = True):
        """Set result image (preview or full-size)."""
        if is_preview:
            self.preview_image = image
        else:
            self.result_image = image
    
    def get_result_for_save(self) -> Optional[np.ndarray]:
        """Get result image for saving (full-size or original if no result)."""
        if self.result_image is not None:
            return self.result_image
        return self.original_image
    
    def reset(self):
        """Reset to original state."""
        if self.original_image is not None:
            self._create_preview()
            self.result_image = None
    
    def get_size(self) -> Tuple[int, int]:
        """Get original image size."""
        if self.original_size:
            return self.original_size
        return (0, 0)
    
    def get_format(self) -> str:
        """Get image format."""
        return self.image_format or 'PNG'

