"""Log panel for displaying application logs."""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, QPushButton,
                             QHBoxLayout, QLabel)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCharFormat, QColor, QTextCursor


class LogPanel(QWidget):
    """Panel for displaying application logs."""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Logs")
        title.setStyleSheet("font-weight: bold; padding: 5px; color: #cccccc;")
        header_layout.addWidget(title)
        
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear)
        header_layout.addWidget(clear_btn)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Log text area
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFontFamily("Consolas")
        self.log_text.setFontPointSize(9)
        self.log_text.setStyleSheet("background-color: #1e1e1e; color: #cccccc; border: 1px solid #3c3c3c;")
        layout.addWidget(self.log_text)
        
        self.setLayout(layout)
    
    def add_log(self, log_entry: dict):
        """Add a log entry."""
        time = log_entry.get("time", "")
        level = log_entry.get("level", "INFO")
        message = log_entry.get("message", "")
        
        # Format log line
        log_line = f"[{time}] {level}: {message}\n"
        
        # Set color based on level
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        format = QTextCharFormat()
        if level == "ERROR":
            format.setForeground(QColor(255, 100, 100))  # Red for errors
        elif level == "WARN":
            format.setForeground(QColor(255, 200, 100))  # Orange for warnings
        else:
            format.setForeground(QColor(200, 200, 200))  # Light gray for info
        
        cursor.insertText(log_line, format)
        self.log_text.setTextCursor(cursor)
        self.log_text.ensureCursorVisible()
    
    def clear(self):
        """Clear all logs."""
        self.log_text.clear()

