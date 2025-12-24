"""Effect stack panel for managing applied effects."""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
                             QPushButton, QHBoxLayout, QCheckBox, QLabel)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from typing import List
from app.core.pipeline import EffectInstance


class EffectStackWidget(QWidget):
    """Widget for displaying and managing effect stack."""
    
    effect_toggled = pyqtSignal(int, bool)  # index, enabled
    effect_removed = pyqtSignal(int)  # index
    effect_moved = pyqtSignal(int, int)  # from_index, to_index
    
    def __init__(self):
        super().__init__()
        self.current_effects = []
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout()
        
        title = QLabel("Effect Stack")
        title.setStyleSheet("font-weight: bold; padding: 5px; color: #cccccc;")
        layout.addWidget(title)
        
        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.list_widget.model().rowsMoved.connect(self.on_rows_moved)
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        layout.addWidget(self.list_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.clicked.connect(self.on_clear)
        button_layout.addWidget(self.clear_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def update_stack(self, effects: List[EffectInstance]):
        """Update the stack display."""
        self.list_widget.clear()
        self.current_effects = effects
        
        for i, effect in enumerate(effects):
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, i)
            
            # Create widget for item
            widget = QWidget()
            widget_layout = QHBoxLayout()
            widget_layout.setContentsMargins(5, 2, 5, 2)
            
            # Checkbox - use a factory function to capture the correct index
            def make_checkbox_handler(idx):
                return lambda state: self.effect_toggled.emit(idx, state == Qt.CheckState.Checked.value)
            
            checkbox = QCheckBox()
            checkbox.setChecked(effect.enabled)
            checkbox.stateChanged.connect(make_checkbox_handler(i))
            widget_layout.addWidget(checkbox)
            
            # Effect name
            name_label = QLabel(effect.name)
            name_label.setStyleSheet("font-weight: bold; color: #cccccc;")
            widget_layout.addWidget(name_label)
            
            widget_layout.addStretch()
            
            # Remove button - use a factory function to capture the correct index
            def make_remove_handler(idx):
                return lambda checked: self.effect_removed.emit(idx)
            
            remove_btn = QPushButton("×")
            remove_btn.setMaximumWidth(30)
            remove_btn.clicked.connect(make_remove_handler(i))
            widget_layout.addWidget(remove_btn)
            
            widget.setLayout(widget_layout)
            
            item.setSizeHint(widget.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, widget)
    
    def get_current_order(self):
        """Get current order of effects from list widget."""
        order = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            widget = self.list_widget.itemWidget(item)
            if widget:
                # Find the effect name label
                for child in widget.findChildren(QLabel):
                    if child.text() and child.text() != "×":
                        order.append(child.text())
                        break
        return order
    
    def on_rows_moved(self, parent, start, end, destination, row):
        """Handle row movement (drag and drop)."""
        # Calculate actual destination index
        if row <= start:
            to_index = row
        else:
            to_index = row - (end - start + 1)
        
        from_index = start
        
        # Emit signal to update pipeline
        self.effect_moved.emit(from_index, to_index)
    
    def on_item_double_clicked(self, item: QListWidgetItem):
        """Handle double click on item."""
        # Could open effect editor
        pass
    
    def on_clear(self):
        """Clear all effects."""
        self.list_widget.clear()

