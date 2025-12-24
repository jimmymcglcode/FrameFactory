"""Dark theme styles for PixelLab."""
DARK_THEME_STYLE = """
QMainWindow {
    background-color: #1e1e1e;
    color: #ffffff;
}

QWidget {
    background-color: #1e1e1e;
    color: #ffffff;
    font-size: 10pt;
}

QMenuBar {
    background-color: #252526;
    color: #cccccc;
    border: none;
}

QMenuBar::item {
    background-color: transparent;
    padding: 4px 8px;
}

QMenuBar::item:selected {
    background-color: #2a2d2e;
}

QMenu {
    background-color: #252526;
    color: #cccccc;
    border: 1px solid #3c3c3c;
}

QMenu::item:selected {
    background-color: #094771;
}

QToolBar {
    background-color: #252526;
    border: none;
    spacing: 3px;
    padding: 3px;
}

QToolBar QToolButton {
    background-color: #2a2d2e;
    color: #cccccc;
    border: 1px solid #3c3c3c;
    border-radius: 3px;
    padding: 5px 10px;
}

QToolBar QToolButton:hover {
    background-color: #3c3c3c;
}

QToolBar QToolButton:pressed {
    background-color: #094771;
}

QPushButton {
    background-color: #0e639c;
    color: #ffffff;
    border: 1px solid #007acc;
    border-radius: 3px;
    padding: 5px 15px;
    min-width: 80px;
}

QPushButton:hover {
    background-color: #1177bb;
}

QPushButton:pressed {
    background-color: #005a9e;
}

QPushButton:disabled {
    background-color: #2a2d2e;
    color: #6a6a6a;
    border: 1px solid #3c3c3c;
}

QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #1e1e1e;
    color: #cccccc;
    border: 1px solid #3c3c3c;
    border-radius: 3px;
    padding: 4px;
    selection-background-color: #094771;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #007acc;
}

QComboBox {
    background-color: #1e1e1e;
    color: #cccccc;
    border: 1px solid #3c3c3c;
    border-radius: 3px;
    padding: 4px;
    min-width: 100px;
}

QComboBox:hover {
    border: 1px solid #007acc;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #cccccc;
    width: 0;
    height: 0;
}

QComboBox QAbstractItemView {
    background-color: #252526;
    color: #cccccc;
    selection-background-color: #094771;
    border: 1px solid #3c3c3c;
}

QSpinBox, QDoubleSpinBox {
    background-color: #1e1e1e;
    color: #cccccc;
    border: 1px solid #3c3c3c;
    border-radius: 3px;
    padding: 4px;
    min-width: 60px;
}

QSpinBox:focus, QDoubleSpinBox:focus {
    border: 1px solid #007acc;
}

QSpinBox::up-button, QDoubleSpinBox::up-button {
    background-color: #2a2d2e;
    border-left: 1px solid #3c3c3c;
    width: 16px;
}

QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover {
    background-color: #3c3c3c;
}

QSpinBox::down-button, QDoubleSpinBox::down-button {
    background-color: #2a2d2e;
    border-left: 1px solid #3c3c3c;
    width: 16px;
}

QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {
    background-color: #3c3c3c;
}

QCheckBox {
    color: #cccccc;
    spacing: 5px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #3c3c3c;
    background-color: #1e1e1e;
    border-radius: 3px;
}

QCheckBox::indicator:hover {
    border: 1px solid #007acc;
}

QCheckBox::indicator:checked {
    background-color: #0e639c;
    border: 1px solid #007acc;
    image: none;
}

QCheckBox::indicator:checked::after {
    content: "✓";
    color: white;
    font-weight: bold;
}

QSlider::groove:horizontal {
    border: 1px solid #3c3c3c;
    height: 6px;
    background: #2a2d2e;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: #0e639c;
    border: 1px solid #007acc;
    width: 18px;
    margin: -6px 0;
    border-radius: 9px;
}

QSlider::handle:horizontal:hover {
    background: #1177bb;
}

QTabWidget::pane {
    border: 1px solid #3c3c3c;
    background-color: #1e1e1e;
}

QTabBar::tab {
    background-color: #2a2d2e;
    color: #cccccc;
    border: 1px solid #3c3c3c;
    padding: 6px 12px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #1e1e1e;
    border-bottom: 2px solid #007acc;
}

QTabBar::tab:hover {
    background-color: #3c3c3c;
}

QGroupBox {
    border: 1px solid #3c3c3c;
    border-radius: 3px;
    margin-top: 10px;
    padding-top: 10px;
    color: #cccccc;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 5px;
    background-color: #1e1e1e;
}

QScrollArea {
    border: 1px solid #3c3c3c;
    background-color: #1e1e1e;
}

QScrollBar:vertical {
    background-color: #1e1e1e;
    width: 12px;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: #3c3c3c;
    min-height: 20px;
    border-radius: 6px;
}

QScrollBar::handle:vertical:hover {
    background-color: #4a4a4a;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #1e1e1e;
    height: 12px;
    border: none;
}

QScrollBar::handle:horizontal {
    background-color: #3c3c3c;
    min-width: 20px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #4a4a4a;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

QListWidget {
    background-color: #1e1e1e;
    color: #cccccc;
    border: 1px solid #3c3c3c;
    border-radius: 3px;
}

QListWidget::item {
    padding: 4px;
    border-bottom: 1px solid #2a2d2e;
}

QListWidget::item:selected {
    background-color: #094771;
    color: #ffffff;
}

QListWidget::item:hover {
    background-color: #2a2d2e;
}

QStatusBar {
    background-color: #007acc;
    color: #ffffff;
    border-top: 1px solid #3c3c3c;
}

QStatusBar::item {
    border: none;
}

QLabel {
    color: #cccccc;
}

QSplitter::handle {
    background-color: #2a2d2e;
}

QSplitter::handle:horizontal {
    width: 3px;
}

QSplitter::handle:vertical {
    height: 3px;
}

QSplitter::handle:hover {
    background-color: #3c3c3c;
}
"""

