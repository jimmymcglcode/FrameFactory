"""Loading overlay widget."""
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPainter, QColor
import time


class LoadingOverlay(QWidget):
    """Semi-transparent overlay with loading indicator and progress."""
    
    cancelled = pyqtSignal()  # Signal emitted when cancel button is clicked
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.hide()
        
        # Animation
        self.angle = 0
        self.start_time = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.setInterval(100)  # Update every 100ms for time display
        
        # Estimated time (can be set externally)
        self.estimated_time = None  # in seconds
        
        # Time label (overlay on top)
        self.time_label = QLabel("Обработка...", self)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet("""
            background-color: transparent;
            color: #ffffff; 
            font-size: 16px; 
            font-weight: bold; 
            padding: 10px;
        """)
        self.time_label.hide()
        
        # Progress info label (overlay on top)
        self.progress_label = QLabel("", self)
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_label.setStyleSheet("""
            background-color: transparent;
            color: #cccccc; 
            font-size: 12px; 
            padding: 5px;
        """)
        self.progress_label.hide()
        
        # Cancel button
        self.cancel_button = QPushButton("Отмена", self)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: #ffffff;
                border: none;
                padding: 8px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
            QPushButton:pressed {
                background-color: #8b0000;
            }
        """)
        self.cancel_button.clicked.connect(self.cancelled.emit)
        self.cancel_button.hide()
    
    def show_loading(self, estimated_time=None, custom_text=None):
        """Show loading overlay with optional estimated time in seconds."""
        if self.parent():
            parent_rect = self.parent().rect()
            self.setGeometry(0, 0, parent_rect.width(), parent_rect.height())
        self.raise_()  # Bring to front
        self.show()
        self.start_time = time.time()
        self.estimated_time = estimated_time
        
        if custom_text:
            self.time_label.setText(custom_text)
        else:
            self.time_label.setText("Обработка...")
        
        self.timer.start()
        self.angle = 0
        
        # Position labels
        self.update_label_positions()
        self.time_label.show()
        self.progress_label.show()
        self.cancel_button.show()
        self.update()
    
    def resizeEvent(self, event):
        """Handle resize to update label positions."""
        super().resizeEvent(event)
        if self.isVisible():
            self.update_label_positions()
    
    def update_label_positions(self):
        """Update label positions based on widget size."""
        if not self.isVisible() and not hasattr(self, 'time_label'):
            return
        center_x = self.width() // 2
        center_y = self.height() // 2
        
        # Time label - above center (wider to prevent text truncation)
        self.time_label.setGeometry(
            center_x - 300, center_y - 60,
            600, 30
        )
        
        # Progress label - below time label (wider to prevent text truncation)
        self.progress_label.setGeometry(
            center_x - 300, center_y - 20,
            600, 30
        )
        
        # Cancel button - below progress label
        button_width = 120
        button_height = 35
        self.cancel_button.setGeometry(
            center_x - button_width // 2, center_y + 20,
            button_width, button_height
        )
    
    def hide_loading(self):
        """Hide loading overlay."""
        self.hide()
        self.timer.stop()
        self.start_time = None
        self.estimated_time = None
        self.time_label.hide()
        self.progress_label.hide()
        self.cancel_button.hide()
    
    def update_animation(self):
        """Update rotation angle and time display."""
        self.angle = (self.angle + 18) % 360  # 18 degrees per frame
        
        if self.start_time:
            elapsed = time.time() - self.start_time
            
            # Update time label
            if elapsed < 1:
                time_text = f"Обработка... {elapsed*1000:.0f} мс"
            elif elapsed < 60:
                time_text = f"Обработка... {elapsed:.1f} сек"
            else:
                minutes = int(elapsed // 60)
                seconds = int(elapsed % 60)
                time_text = f"Обработка... {minutes} мин {seconds} сек"
            
            self.time_label.setText(time_text)
            
            # Update progress info
            if self.estimated_time and self.estimated_time > 0:
                progress = min(elapsed / self.estimated_time, 0.99)  # Max 99% until done
                remaining = max(0, self.estimated_time - elapsed)
                
                if remaining < 1:
                    progress_text = f"Осталось: < 1 сек"
                elif remaining < 60:
                    progress_text = f"Осталось: ~{remaining:.1f} сек ({progress*100:.0f}%)"
                else:
                    rem_min = int(remaining // 60)
                    rem_sec = int(remaining % 60)
                    progress_text = f"Осталось: ~{rem_min} мин {rem_sec} сек ({progress*100:.0f}%)"
            else:
                # Estimate based on elapsed time (rough estimate: first second = 20% progress)
                if elapsed < 1:
                    estimated_total = elapsed / 0.2
                    remaining = max(0, estimated_total - elapsed)
                    progress_text = f"Примерно: < {estimated_total:.1f} сек"
                else:
                    # After 1 second, estimate increases linearly
                    estimated_total = elapsed * 1.5  # Conservative estimate
                    remaining = max(0, estimated_total - elapsed)
                    if remaining < 1:
                        progress_text = "Завершение..."
                    elif remaining < 60:
                        progress_text = f"Примерно осталось: ~{remaining:.1f} сек"
                    else:
                        rem_min = int(remaining // 60)
                        rem_sec = int(remaining % 60)
                        progress_text = f"Примерно осталось: ~{rem_min} мин {rem_sec} сек"
            
            self.progress_label.setText(progress_text)
        
        self.update()
    
    def paintEvent(self, event):
        """Paint loading indicator."""
        if not self.isVisible():
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Semi-transparent background
        painter.fillRect(self.rect(), QColor(0, 0, 0, 200))
        
        # Loading spinner (drawn behind text)
        center_x = self.width() // 2
        center_y = self.height() // 2 - 80  # Move up to make room for text and button
        radius = 35
        
        # Draw spinner circle background
        painter.setPen(QColor(100, 100, 100, 100))
        painter.setBrush(QColor(50, 50, 50, 50))
        painter.drawEllipse(center_x - radius - 5, center_y - radius - 5, (radius + 5) * 2, (radius + 5) * 2)
        
        # Draw 8 dots in circle
        import math
        for i in range(8):
            angle_deg = (self.angle + i * 45) % 360
            angle_rad = math.radians(angle_deg)
            x = center_x + radius * 0.8 * math.cos(angle_rad)
            y = center_y + radius * 0.8 * math.sin(angle_rad)
            
            # Fade based on position
            alpha = int(255 * (0.4 + 0.6 * (i / 8)))
            painter.setBrush(QColor(100, 150, 255, alpha))
            painter.setPen(QColor(100, 150, 255, alpha))
            painter.drawEllipse(int(x - 6), int(y - 6), 12, 12)
