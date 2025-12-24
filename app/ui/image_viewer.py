"""Image viewer widget."""
from PyQt6.QtWidgets import QWidget, QLabel, QScrollArea, QVBoxLayout
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QImage, QPixmap
import numpy as np


class ImageViewer(QWidget):
    """Widget for displaying images with zoom support."""
    
    ZOOM_FIT = "fit"
    ZOOM_100 = "100%"
    ZOOM_200 = "200%"
    
    def __init__(self, title="Image"):
        super().__init__()
        self.title = title
        self.image: np.ndarray = None
        self.current_zoom = self.ZOOM_FIT
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title label
        self.title_label = QLabel(self.title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-weight: bold; padding: 5px; color: #cccccc; background-color: #252526; border-bottom: 1px solid #3c3c3c;")
        layout.addWidget(self.title_label)
        
        # Scroll area for image
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(100, 100)
        self.image_label.setText("No image")
        self.scroll_area.setWidget(self.image_label)
        
        layout.addWidget(self.scroll_area)
        self.setLayout(layout)
    
    def set_image(self, image: np.ndarray):
        """Set image to display."""
        if image is None:
            self.image_label.setText("No image")
            self.image = None
            return
        
        self.image = image
        self.update_display()
    
    def set_zoom(self, zoom_mode: str):
        """Set zoom mode."""
        self.current_zoom = zoom_mode
        self.update_display()
    
    def update_display(self):
        """Update displayed image based on current zoom."""
        if self.image is None:
            return
        
        h, w = self.image.shape[:2]
        
        # Calculate display size based on zoom
        if self.current_zoom == self.ZOOM_FIT:
            # Fit to widget size
            scroll_size = self.scroll_area.size()
            available_w = scroll_size.width() - 20
            available_h = scroll_size.height() - 20
            
            if available_w > 0 and available_h > 0:
                scale_w = available_w / w
                scale_h = available_h / h
                scale = min(scale_w, scale_h, 1.0)  # Don't upscale
                display_w = int(w * scale)
                display_h = int(h * scale)
            else:
                display_w, display_h = w, h
        elif self.current_zoom == self.ZOOM_100:
            display_w, display_h = w, h
        elif self.current_zoom == self.ZOOM_200:
            display_w, display_h = w * 2, h * 2
        else:
            display_w, display_h = w, h
        
        # Convert numpy array to QPixmap using PIL for safety
        from PIL import Image as PILImage
        
        # Ensure contiguous array
        image_copy = np.ascontiguousarray(self.image, dtype=np.uint8)
        
        # Convert to PIL Image
        if len(image_copy.shape) == 2:
            pil_image = PILImage.fromarray(image_copy, mode='L')
        else:
            pil_image = PILImage.fromarray(image_copy, mode='RGB')
        
        # Convert PIL Image to QImage via temporary bytes
        import io
        buffer = io.BytesIO()
        pil_image.save(buffer, format='PNG')
        buffer.seek(0)
        qimage = QImage.fromData(buffer.read())
        
        # Scale image
        pixmap = QPixmap.fromImage(qimage)
        scaled_pixmap = pixmap.scaled(
            display_w, display_h,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.resize(scaled_pixmap.size())
    
    def resizeEvent(self, event):
        """Handle resize event."""
        super().resizeEvent(event)
        if self.current_zoom == self.ZOOM_FIT:
            self.update_display()

