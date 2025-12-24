"""Effect panel for selecting and configuring effects."""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QGroupBox,
                             QLabel, QSlider, QSpinBox, QDoubleSpinBox,
                             QComboBox, QCheckBox, QPushButton, QHBoxLayout,
                             QFormLayout, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Dict, Any, Type
from app.effects.base import Effect


class EffectPanel(QWidget):
    """Panel for selecting and configuring effects."""
    
    apply_effect = pyqtSignal(object, dict)  # effect_class, params
    
    def __init__(self, effect_groups: Dict[str, list]):
        super().__init__()
        self.effect_groups = effect_groups
        self.current_effect_class: Type[Effect] = None
        self.param_widgets: Dict[str, Any] = {}
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout()
        
        # Tabs for effect groups
        self.tabs = QTabWidget()
        for group_name, effects in self.effect_groups.items():
            tab_widget = QWidget()
            tab_layout = QVBoxLayout()
            tab_layout.setSpacing(10)
            
            # Effect buttons
            for effect_class in effects:
                btn = QPushButton(effect_class.name)
                btn.setToolTip(effect_class.description)
                btn.clicked.connect(lambda checked, ec=effect_class: self.select_effect(ec))
                tab_layout.addWidget(btn)
            
            tab_layout.addStretch()
            tab_widget.setLayout(tab_layout)
            
            scroll = QScrollArea()
            scroll.setWidget(tab_widget)
            scroll.setWidgetResizable(True)
            
            self.tabs.addTab(scroll, group_name)
        
        layout.addWidget(self.tabs)
        
        # Current effect configuration
        self.config_group = QGroupBox("Effect Parameters")
        self.config_layout = QVBoxLayout()
        self.config_group.setLayout(self.config_layout)
        layout.addWidget(self.config_group)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        self.randomize_btn = QPushButton("Randomize")
        self.randomize_btn.clicked.connect(self.on_randomize)
        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(self.on_apply)
        button_layout.addWidget(self.randomize_btn)
        button_layout.addWidget(self.apply_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Hide config initially
        self.config_group.setVisible(False)
    
    def select_effect(self, effect_class: Type[Effect]):
        """Select an effect and show its parameters."""
        self.current_effect_class = effect_class
        
        # Clear existing widgets
        self.clear_config()
        self.param_widgets.clear()
        
        # Get default params
        params = effect_class.default_params()
        
        # Create parameter widgets
        form_layout = QFormLayout()
        
        for param_name, param_value in params.items():
            widget, label_text = self.create_param_widget(param_name, param_value, effect_class)
            if widget:
                self.param_widgets[param_name] = widget
                form_layout.addRow(label_text, widget)
        
        self.config_layout.addLayout(form_layout)
        
        # Add description
        desc_label = QLabel(effect_class.description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("font-style: italic; color: #888; padding: 5px;")
        self.config_layout.insertWidget(0, desc_label)
        
        self.config_group.setTitle(f"Parameters: {effect_class.name}")
        self.config_group.setVisible(True)
    
    def create_param_widget(self, param_name: str, param_value: Any, effect_class: Type[Effect] = None):
        """Create appropriate widget for parameter."""
        label_text = param_name.replace("_", " ").title()
        
        if isinstance(param_value, bool):
            widget = QCheckBox()
            widget.setChecked(param_value)
            return widget, label_text
        
        elif isinstance(param_value, int):
            # Determine range based on param name
            if "shift" in param_name.lower() or "amount" in param_name.lower():
                widget = QSpinBox()
                widget.setRange(-1000, 1000)
            elif "seed" in param_name.lower():
                widget = QSpinBox()
                widget.setRange(0, 2**31 - 1)
            elif "level" in param_name.lower() or "size" in param_name.lower():
                widget = QSpinBox()
                widget.setRange(1, 1000)
            elif "rotation" in param_name.lower():
                widget = QSpinBox()
                widget.setRange(0, 270)
                widget.setSingleStep(90)
            else:
                widget = QSpinBox()
                widget.setRange(-10000, 10000)
            widget.setValue(param_value)
            return widget, label_text
        
        elif isinstance(param_value, float):
            widget = QDoubleSpinBox()
            # Adjust range based on param name
            if "saturation" in param_name.lower() or "value" in param_name.lower() or "brightness" in param_name.lower():
                widget.setRange(0.0, 2.0)
            elif "gamma" in param_name.lower():
                widget.setRange(0.2, 3.0)
            elif "exposure" in param_name.lower():
                widget.setRange(-2.0, 2.0)
            elif "smoothness" in param_name.lower() or "amount" in param_name.lower() or "strength" in param_name.lower():
                widget.setRange(0.0, 1.0)
            elif "sigma" in param_name.lower():
                widget.setRange(0.0, 10.0)
            else:
                widget.setRange(-1000.0, 1000.0)
            widget.setSingleStep(0.1)
            widget.setDecimals(2)
            widget.setValue(param_value)
            return widget, label_text
        
        elif isinstance(param_value, str):
            # Use combobox for string parameters
            widget = QComboBox()
            widget.setEditable(False)
            
            # Populate choices based on param name and effect
            if effect_class:
                self.populate_combobox_choices(param_name, widget, effect_class)
            else:
                widget.addItem(param_value)
            
            if widget.findText(param_value) >= 0:
                widget.setCurrentText(param_value)
            else:
                widget.addItem(param_value)
                widget.setCurrentText(param_value)
            
            return widget, label_text
        
        return None, label_text
    
    def populate_combobox_choices(self, param_name: str, widget: QComboBox, effect_class: Type[Effect]):
        """Populate combobox with valid choices based on effect."""
        params = effect_class.default_params()
        default_value = params.get(param_name, "")
        
        # Define choices for common parameters
        choices_map = {
            "direction": ["rows", "columns", "both"],
            "wrap_mode": ["wrap", "reflect", "clamp"],
            "interpolation": ["nearest", "bilinear", "bicubic", "lanczos"],
            "type": ["wave", "noise"],
            "mode": ["blur", "sharpen", "percent", "absolute", "rgb", "rbg", "grb", "gbr", "brg", "bgr", "mix"],
            "block_transform": ["none", "rotate", "flip", "jitter"],
        }
        
        # Check specific parameter names
        param_lower = param_name.lower()
        choices = None
        
        for key, values in choices_map.items():
            if key in param_lower:
                choices = values
                break
        
        # Special cases for mode parameter
        if "mode" in param_lower:
            if "channel" in str(effect_class.name).lower():
                choices = ["rgb", "rbg", "grb", "gbr", "brg", "bgr", "mix"]
            elif "sharpen" in str(effect_class.name).lower() or "blur" in str(effect_class.name).lower():
                choices = ["blur", "sharpen"]
            elif "crop" in str(effect_class.name).lower():
                choices = ["percent", "absolute"]
        
        if choices is None:
            choices = [default_value] if default_value else []
        
        widget.clear()
        widget.addItems(choices)
        if default_value in choices:
            widget.setCurrentText(default_value)
        elif choices:
            widget.setCurrentIndex(0)
    
    def clear_config(self):
        """Clear configuration widgets."""
        while self.config_layout.count():
            item = self.config_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())
    
    def clear_layout(self, layout):
        """Recursively clear layout."""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())
    
    def get_params(self) -> Dict[str, Any]:
        """Get current parameter values."""
        params = {}
        for param_name, widget in self.param_widgets.items():
            if isinstance(widget, QCheckBox):
                params[param_name] = widget.isChecked()
            elif isinstance(widget, QSpinBox):
                params[param_name] = widget.value()
            elif isinstance(widget, QDoubleSpinBox):
                params[param_name] = widget.value()
            elif isinstance(widget, QComboBox):
                params[param_name] = widget.currentText()
        return params
    
    def set_params(self, params: Dict[str, Any]):
        """Set parameter values."""
        for param_name, value in params.items():
            if param_name in self.param_widgets:
                widget = self.param_widgets[param_name]
                if isinstance(widget, QCheckBox):
                    widget.setChecked(value)
                elif isinstance(widget, QSpinBox):
                    widget.setValue(int(value))
                elif isinstance(widget, QDoubleSpinBox):
                    widget.setValue(float(value))
                elif isinstance(widget, QComboBox):
                    widget.setCurrentText(str(value))
    
    def on_randomize(self):
        """Randomize current effect parameters."""
        if self.current_effect_class:
            import random
            seed = random.randint(0, 2**31 - 1)
            params = self.current_effect_class.randomize(
                self.current_effect_class.default_params(),
                seed
            )
            self.set_params(params)
    
    def on_apply(self):
        """Apply current effect with current parameters."""
        if self.current_effect_class:
            params = self.get_params()
            self.apply_effect.emit(self.current_effect_class, params)

