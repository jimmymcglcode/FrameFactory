"""Loading overlay widget."""
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor


class LoadingOverlay(QWidget):
    """Semi-transparent overlay with loading indicator."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.hide()
        
        # Animation
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.setInterval(50)  # ~20 FPS
    
    def show_loading(self):
        """Show loading overlay."""
        if self.parent():
            self.setGeometry(self.parent().rect())
        self.show()
        self.timer.start()
        self.angle = 0
    
    def hide_loading(self):
        """Hide loading overlay."""
        self.hide()
        self.timer.stop()
    
    def update_animation(self):
        """Update rotation angle."""
        self.angle = (self.angle + 18) % 360  # 18 degrees per frame = 360 in 20 frames
        self.update()
    
    def paintEvent(self, event):
        """Paint loading indicator."""
        if not self.isVisible():
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Semi-transparent background
        painter.fillRect(self.rect(), QColor(0, 0, 0, 180))
        
        # Loading spinner
        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = 30
        
        painter.setPen(QColor(255, 255, 255, 0))
        painter.setBrush(QColor(100, 150, 255, 200))
        
        # Draw 8 dots in circle
        import math
        for i in range(8):
            angle_deg = (self.angle + i * 45) % 360
            angle_rad = math.radians(angle_deg)
            x = center_x + radius * 0.7 * math.cos(angle_rad)
            y = center_y + radius * 0.7 * math.sin(angle_rad)
            
            # Fade based on position
            alpha = int(255 * (0.3 + 0.7 * (i / 8)))
            painter.setBrush(QColor(100, 150, 255, alpha))
            painter.drawEllipse(int(x - 5), int(y - 5), 10, 10)
        
        # Text
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(painter.font())
        text = "Обработка..."
        text_rect = painter.fontMetrics().boundingRect(text)
        painter.drawText(
            center_x - text_rect.width() // 2,
            center_y + radius + 20,
            text
        )

