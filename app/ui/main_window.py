"""Main window for PixelLab."""
import time
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QMenuBar, QMenu, QToolBar, QStatusBar, QLabel,
                             QSplitter, QFileDialog, QMessageBox, QComboBox,
                             QPushButton, QTabWidget, QApplication)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QAction, QKeySequence, QIcon
import numpy as np
from PIL import Image

from app.core.image_model import ImageModel
from app.core.pipeline import Pipeline
from app.core.preset import PresetManager
from app.core.logger import logger
from app.effects.registry import EFFECT_REGISTRY, EFFECT_GROUPS

from app.ui.image_viewer import ImageViewer
from app.ui.effect_panel import EffectPanel
from app.ui.effect_stack import EffectStackWidget
from app.ui.log_panel import LogPanel
from app.ui.help_dialog import HelpDialog
from app.ui.loading_overlay import LoadingOverlay
from app.ui.theme import DARK_THEME_STYLE


class ProcessingThread(QThread):
    """Thread for processing images to avoid UI blocking."""
    finished = pyqtSignal(np.ndarray)
    error = pyqtSignal(str)
    
    def __init__(self, image: np.ndarray, pipeline: Pipeline):
        super().__init__()
        self.image = image.copy()  # Make a copy to avoid issues
        self.pipeline = pipeline
    
    def run(self):
        """Process image in background thread."""
        try:
            result = self.pipeline.apply(self.image)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.image_model = ImageModel()
        self.pipeline = Pipeline()
        self.preset_manager = PresetManager(EFFECT_REGISTRY)
        self.processing_thread = None
        self.is_processing = False
        
        # Setup logger callback
        logger.set_log_callback(self.on_log_entry)
        
        self.setup_ui()
        self.update_undo_redo_buttons()
        self.update_preview()
        
        logger.info("PixelLab started")
    
    def setup_ui(self):
        """Setup main window UI."""
        self.setWindowTitle("PixelLab")
        self.setGeometry(100, 100, 1400, 900)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create main splitter
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left: Image viewers
        image_splitter = QSplitter(Qt.Orientation.Vertical)
        self.original_viewer = ImageViewer("Original")
        self.preview_viewer = ImageViewer("Preview")
        image_splitter.addWidget(self.original_viewer)
        image_splitter.addWidget(self.preview_viewer)
        image_splitter.setSizes([300, 300])
        main_splitter.addWidget(image_splitter)
        
        # Right: Effects and stack
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)
        
        # Effect panel
        self.effect_panel = EffectPanel(EFFECT_GROUPS)
        self.effect_panel.apply_effect.connect(self.on_apply_effect)
        right_layout.addWidget(self.effect_panel)
        
        # Effect stack
        self.effect_stack = EffectStackWidget()
        self.effect_stack.effect_toggled.connect(self.on_effect_toggled)
        self.effect_stack.effect_removed.connect(self.on_effect_removed)
        self.effect_stack.effect_moved.connect(self.on_effect_moved)
        right_layout.addWidget(self.effect_stack)
        
        main_splitter.addWidget(right_widget)
        main_splitter.setSizes([800, 400])
        
        main_layout.addWidget(main_splitter)
        
        # Create status bar
        self.create_status_bar()
        
        # Create log tab
        self.log_panel = LogPanel()
        
        # Add loading overlay to central widget
        self.loading_overlay = LoadingOverlay(central_widget)
        self.loading_overlay.hide()
    
    def create_menu_bar(self):
        """Create menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        open_action = QAction("Open...", self)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.triggered.connect(self.on_open)
        file_menu.addAction(open_action)
        
        save_action = QAction("Save As...", self)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.triggered.connect(self.on_save)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        save_preset_action = QAction("Save Preset...", self)
        save_preset_action.triggered.connect(self.on_save_preset)
        file_menu.addAction(save_preset_action)
        
        load_preset_action = QAction("Load Preset...", self)
        load_preset_action.triggered.connect(self.on_load_preset)
        file_menu.addAction(load_preset_action)
        
        random_preset_action = QAction("Random Preset", self)
        random_preset_action.triggered.connect(self.on_random_preset)
        file_menu.addAction(random_preset_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence("Alt+F4"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        undo_action = QAction("Undo", self)
        undo_action.setShortcut(QKeySequence("Ctrl+Z"))
        undo_action.triggered.connect(self.on_undo)
        edit_menu.addAction(undo_action)
        self.undo_action = undo_action
        
        redo_action = QAction("Redo", self)
        redo_action.setShortcut(QKeySequence("Ctrl+Y"))
        redo_action.triggered.connect(self.on_redo)
        edit_menu.addAction(redo_action)
        self.redo_action = redo_action
        
        edit_menu.addSeparator()
        
        reset_action = QAction("Reset", self)
        reset_action.triggered.connect(self.on_reset)
        edit_menu.addAction(reset_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        logs_action = QAction("Show Logs", self)
        logs_action.triggered.connect(self.show_logs)
        view_menu.addAction(logs_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        help_action = QAction("Справка", self)
        help_action.setShortcut(QKeySequence("F1"))
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)
        
        help_menu.addSeparator()
        
        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """Create toolbar."""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        open_btn = QPushButton("Open")
        open_btn.clicked.connect(self.on_open)
        toolbar.addWidget(open_btn)
        
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.on_save)
        toolbar.addWidget(save_btn)
        
        toolbar.addSeparator()
        
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self.on_reset)
        toolbar.addWidget(reset_btn)
        
        undo_btn = QPushButton("Undo")
        undo_btn.clicked.connect(self.on_undo)
        toolbar.addWidget(undo_btn)
        
        redo_btn = QPushButton("Redo")
        redo_btn.clicked.connect(self.on_redo)
        toolbar.addWidget(redo_btn)
        
        toolbar.addSeparator()
        
        # Zoom controls
        zoom_label = QLabel("Zoom:")
        toolbar.addWidget(zoom_label)
        
        self.zoom_combo = QComboBox()
        self.zoom_combo.addItems(["Fit", "100%", "200%"])
        self.zoom_combo.currentTextChanged.connect(self.on_zoom_changed)
        toolbar.addWidget(self.zoom_combo)
    
    def create_status_bar(self):
        """Create status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.size_label = QLabel("Size: -")
        self.size_label.setStyleSheet("color: #ffffff; padding: 2px 5px;")
        self.format_label = QLabel("Format: -")
        self.format_label.setStyleSheet("color: #ffffff; padding: 2px 5px;")
        self.time_label = QLabel("Time: -")
        self.time_label.setStyleSheet("color: #ffffff; padding: 2px 5px;")
        
        self.status_bar.addPermanentWidget(self.size_label)
        self.status_bar.addPermanentWidget(self.format_label)
        self.status_bar.addPermanentWidget(self.time_label)
        
        self.status_bar.showMessage("Ready")
    
    def on_open(self):
        """Open image file."""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.webp *.bmp *.tiff *.tif);;All Files (*)"
        )
        
        if filepath:
            if self.image_model.load_image(filepath):
                self.original_viewer.set_image(self.image_model.get_preview())
                self.update_status()
                self.update_preview()
                logger.info(f"Opened image: {filepath}")
            else:
                QMessageBox.critical(self, "Error", "Failed to load image")
                logger.error(f"Failed to load image: {filepath}")
    
    def on_save(self):
        """Save processed image."""
        if not self.image_model.has_image():
            QMessageBox.warning(self, "Warning", "No image loaded")
            return
        
        filepath, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Save Image",
            "",
            "PNG (*.png);;JPEG (*.jpg *.jpeg);;WebP (*.webp);;All Files (*)"
        )
        
        if filepath:
            # Show loading indicator
            self.loading_overlay.show_loading()
            self.status_bar.showMessage("Обработка полного разрешения...")
            QApplication.processEvents()  # Update UI
            
            try:
                # Determine format
                if "png" in selected_filter.lower():
                    format = "PNG"
                elif "jpeg" in selected_filter.lower() or "jpg" in selected_filter.lower():
                    format = "JPEG"
                elif "webp" in selected_filter.lower():
                    format = "WEBP"
                else:
                    format = "PNG"
                
                # Process full-size image in background
                original = self.image_model.get_original()
                
                # Use thread for processing large images
                save_thread = ProcessingThread(original, self.pipeline)
                
                def on_save_processing_finished(result: np.ndarray):
                    try:
                        pil_image = Image.fromarray(result)
                        pil_image.save(filepath, format=format)
                        logger.info(f"Saved image: {filepath}")
                        self.status_bar.showMessage(f"Сохранено: {filepath}", 3000)
                        self.loading_overlay.hide_loading()
                        save_thread.quit()
                        save_thread.wait()
                    except Exception as e:
                        QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить изображение: {str(e)}")
                        logger.error(f"Failed to save image: {filepath}", e)
                        self.loading_overlay.hide_loading()
                        save_thread.quit()
                        save_thread.wait()
                
                def on_save_processing_error(error_msg: str):
                    QMessageBox.critical(self, "Ошибка", f"Ошибка обработки: {error_msg}")
                    logger.error(f"Processing error during save: {error_msg}")
                    self.loading_overlay.hide_loading()
                    save_thread.quit()
                    save_thread.wait()
                
                save_thread.finished.connect(on_save_processing_finished)
                save_thread.error.connect(on_save_processing_error)
                save_thread.start()
                
            except Exception as e:
                self.loading_overlay.hide_loading()
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить изображение: {str(e)}")
                logger.error(f"Failed to save image: {filepath}", e)
    
    def on_save_preset(self):
        """Save current preset."""
        pipeline_data = self.pipeline.to_dict()
        
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Save Preset",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if filepath:
            if not filepath.endswith(".json"):
                filepath += ".json"
            
            if self.preset_manager.save_preset(pipeline_data, filepath):
                logger.info(f"Saved preset: {filepath}")
                self.status_bar.showMessage(f"Preset saved: {filepath}", 3000)
            else:
                QMessageBox.critical(self, "Error", "Failed to save preset")
    
    def on_load_preset(self):
        """Load preset."""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Load Preset",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if filepath:
            preset_data = self.preset_manager.load_preset(filepath)
            if preset_data:
                self.pipeline.from_dict(preset_data, EFFECT_REGISTRY)
                self.effect_stack.update_stack(self.pipeline.get_effects())
                self.update_preview()
                logger.info(f"Loaded preset: {filepath}")
                self.status_bar.showMessage(f"Preset loaded: {filepath}", 3000)
            else:
                QMessageBox.critical(self, "Error", "Failed to load preset")
    
    def on_random_preset(self):
        """Generate and apply random preset."""
        preset_data = self.preset_manager.generate_random_preset()
        self.pipeline.from_dict(preset_data, EFFECT_REGISTRY)
        self.effect_stack.update_stack(self.pipeline.get_effects())
        self.update_preview()
        logger.info("Applied random preset")
    
    def on_apply_effect(self, effect_class, params):
        """Apply effect to pipeline."""
        self.pipeline.add_effect(effect_class, params)
        self.effect_stack.update_stack(self.pipeline.get_effects())
        self.update_preview()
        logger.info(f"Applied effect: {effect_class.name}")
    
    def on_effect_toggled(self, index: int, enabled: bool):
        """Toggle effect enabled state."""
        self.pipeline.set_effect_enabled(index, enabled)
        self.update_preview()
    
    def on_effect_removed(self, index: int):
        """Remove effect from pipeline."""
        self.pipeline.remove_effect(index)
        self.effect_stack.update_stack(self.pipeline.get_effects())
        self.update_preview()
    
    def on_effect_moved(self, from_index: int, to_index: int):
        """Move effect in pipeline."""
        self.pipeline.move_effect(from_index, to_index)
        self.effect_stack.update_stack(self.pipeline.get_effects())
        self.update_preview()
    
    def on_undo(self):
        """Undo last change."""
        if self.pipeline.undo():
            self.effect_stack.update_stack(self.pipeline.get_effects())
            self.update_preview()
            self.update_undo_redo_buttons()
            logger.info("Undo")
    
    def on_redo(self):
        """Redo last undone change."""
        if self.pipeline.redo():
            self.effect_stack.update_stack(self.pipeline.get_effects())
            self.update_preview()
            self.update_undo_redo_buttons()
            logger.info("Redo")
    
    def on_reset(self):
        """Reset to original image."""
        self.pipeline.clear()
        self.image_model.reset()
        self.effect_stack.update_stack(self.pipeline.get_effects())
        self.update_preview()
        logger.info("Reset to original")
    
    def on_zoom_changed(self, zoom_text: str):
        """Handle zoom change."""
        zoom_map = {
            "Fit": ImageViewer.ZOOM_FIT,
            "100%": ImageViewer.ZOOM_100,
            "200%": ImageViewer.ZOOM_200,
        }
        zoom = zoom_map.get(zoom_text, ImageViewer.ZOOM_FIT)
        self.original_viewer.set_zoom(zoom)
        self.preview_viewer.set_zoom(zoom)
    
    def update_preview(self):
        """Update preview image in background thread."""
        if not self.image_model.has_image():
            return
        
        preview_image = self.image_model.get_preview()
        if preview_image is None:
            return
        
        # Don't start new processing if one is already running
        if self.is_processing:
            return
        
        # Stop previous thread if exists
        if self.processing_thread and self.processing_thread.isRunning():
            self.processing_thread.terminate()
            self.processing_thread.wait()
        
        # Show loading indicator
        self.loading_overlay.show_loading()
        self.is_processing = True
        
        # Create and start processing thread
        self.processing_thread = ProcessingThread(preview_image, self.pipeline)
        self.processing_thread.finished.connect(self.on_processing_finished)
        self.processing_thread.error.connect(self.on_processing_error)
        self.processing_thread.start()
    
    def on_processing_finished(self, result: np.ndarray):
        """Handle processing completion."""
        start_time = time.time()
        
        # Update model and viewer
        self.image_model.set_result(result, is_preview=True)
        self.preview_viewer.set_image(result)
        
        # Hide loading indicator
        self.loading_overlay.hide_loading()
        self.is_processing = False
        
        # Update status
        processing_time = time.time() - start_time
        self.time_label.setText(f"Time: {processing_time*1000:.1f}ms")
        
        # Clean up thread
        if self.processing_thread:
            self.processing_thread.quit()
            self.processing_thread.wait()
            self.processing_thread = None
    
    def on_processing_error(self, error_msg: str):
        """Handle processing error."""
        self.loading_overlay.hide_loading()
        self.is_processing = False
        
        logger.error(f"Processing error: {error_msg}")
        QMessageBox.warning(self, "Ошибка обработки", f"Произошла ошибка при обработке изображения:\n{error_msg}")
        
        # Clean up thread
        if self.processing_thread:
            self.processing_thread.quit()
            self.processing_thread.wait()
            self.processing_thread = None
    
    def update_status(self):
        """Update status bar information."""
        if self.image_model.has_image():
            w, h = self.image_model.get_size()
            self.size_label.setText(f"Size: {w}x{h}")
            self.format_label.setText(f"Format: {self.image_model.get_format()}")
        else:
            self.size_label.setText("Size: -")
            self.format_label.setText("Format: -")
    
    def update_undo_redo_buttons(self):
        """Update undo/redo button states."""
        self.undo_action.setEnabled(self.pipeline.can_undo())
        self.redo_action.setEnabled(self.pipeline.can_redo())
    
    def on_log_entry(self, log_entry: dict):
        """Handle log entry from logger."""
        if hasattr(self, 'log_panel'):
            self.log_panel.add_log(log_entry)
    
    def show_logs(self):
        """Show log panel in dialog."""
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Logs")
        dialog.setText("Logs are shown in the status bar and console.")
        dialog.exec()
    
    def show_help(self):
        """Show help dialog."""
        help_dialog = HelpDialog(self)
        help_dialog.exec()
    
    def show_about(self):
        """Show about dialog."""
        about_text = """
        <h2>PixelLab</h2>
        <p>Desktop приложение для экспериментов с изображениями</p>
        <p><b>Версия:</b> 1.0</p>
        <p><b>Платформа:</b> Windows (Python 3.11+)</p>
        <hr>
        <p>Координатные и цветовые трансформации с предпросмотром, пресетами и экспортом.</p>
        <p>Нажмите <b>F1</b> или выберите <b>Help → Справка</b> для подробных инструкций.</p>
        """
        QMessageBox.about(self, "О программе", about_text)
    
    def resizeEvent(self, event):
        """Handle window resize to update loading overlay."""
        super().resizeEvent(event)
        if hasattr(self, 'loading_overlay') and self.loading_overlay.isVisible():
            self.loading_overlay.setGeometry(self.rect())

