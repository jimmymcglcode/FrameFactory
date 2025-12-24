"""Main entry point for PixelLab."""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication
from app.ui.main_window import MainWindow
from app.core.logger import logger


def main():
    """Main function."""
    app = QApplication(sys.argv)
    app.setApplicationName("PixelLab")
    
    # Apply dark theme to application
    from app.ui.theme import DARK_THEME_STYLE
    app.setStyleSheet(DARK_THEME_STYLE)
    
    try:
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        logger.error("Fatal error during startup", e)
        sys.exit(1)


if __name__ == "__main__":
    main()

