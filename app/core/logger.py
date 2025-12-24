"""Logging system for PixelLab."""
import logging
import sys
from datetime import datetime
from enum import Enum
from typing import Optional


class LogLevel(Enum):
    """Log levels."""
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"


class Logger:
    """Application logger with UI integration."""
    
    def __init__(self):
        self.logs = []
        self.log_callback = None
        
        # Setup Python logging
        self.py_logger = logging.getLogger("PixelLab")
        self.py_logger.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.py_logger.addHandler(console_handler)
    
    def set_log_callback(self, callback):
        """Set callback for UI log updates."""
        self.log_callback = callback
    
    def log(self, level: LogLevel, message: str, exception: Optional[Exception] = None):
        """Add a log entry."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = {
            "time": timestamp,
            "level": level.value,
            "message": message
        }
        
        if exception:
            import traceback
            log_entry["traceback"] = traceback.format_exc()
            message = f"{message}: {exception}"
        
        self.logs.append(log_entry)
        
        # Python logging
        if level == LogLevel.INFO:
            self.py_logger.info(message)
        elif level == LogLevel.WARN:
            self.py_logger.warning(message)
        elif level == LogLevel.ERROR:
            self.py_logger.error(message, exc_info=exception)
        
        # UI callback
        if self.log_callback:
            self.log_callback(log_entry)
    
    def info(self, message: str):
        """Log info message."""
        self.log(LogLevel.INFO, message)
    
    def warn(self, message: str):
        """Log warning message."""
        self.log(LogLevel.WARN, message)
    
    def error(self, message: str, exception: Optional[Exception] = None):
        """Log error message."""
        self.log(LogLevel.ERROR, message, exception)
    
    def get_logs(self, limit: Optional[int] = None):
        """Get recent logs."""
        if limit:
            return self.logs[-limit:]
        return self.logs
    
    def clear(self):
        """Clear all logs."""
        self.logs.clear()


# Global logger instance
logger = Logger()

