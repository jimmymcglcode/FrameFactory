"""Help dialog with detailed instructions."""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTextEdit,
                             QPushButton, QTabWidget, QWidget, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCharFormat, QColor, QFont


class HelpDialog(QDialog):
    """Help dialog with instructions."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Справка - PixelLab")
        self.setMinimumSize(800, 600)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout()
        
        # Tabs for different sections
        tabs = QTabWidget()
        
        # General instructions
        general_tab = self.create_general_tab()
        tabs.addTab(general_tab, "Общее")
        
        # Effects instructions
        effects_tab = self.create_effects_tab()
        tabs.addTab(effects_tab, "Эффекты")
        
        # Parameters instructions
        params_tab = self.create_parameters_tab()
        tabs.addTab(params_tab, "Параметры")
        
        # Buttons instructions
        buttons_tab = self.create_buttons_tab()
        tabs.addTab(buttons_tab, "Кнопки")
        
        layout.addWidget(tabs)
        
        # Close button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def create_text_widget(self, content: str) -> QTextEdit:
        """Create styled text widget."""
        text_widget = QTextEdit()
        text_widget.setReadOnly(True)
        text_widget.setFont(QFont("Segoe UI", 10))
        text_widget.setStyleSheet("""
            background-color: #1e1e1e;
            color: #cccccc;
            border: 1px solid #3c3c3c;
            padding: 10px;
        """)
        text_widget.setHtml(content)
        return text_widget
    
    def create_general_tab(self) -> QWidget:
        """Create general instructions tab."""
        content = """
        <h2 style="color: #007acc;">Общие инструкции</h2>
        
        <h3 style="color: #0e639c;">Работа с изображениями</h3>
        <p><b>Открытие:</b> Используйте <code>Ctrl+O</code> или кнопку "Open" в toolbar. 
        Поддерживаются форматы: PNG, JPG, JPEG, WebP, BMP, TIFF.</p>
        
        <p><b>Сохранение:</b> Используйте <code>Ctrl+S</code> или кнопку "Save". 
        При сохранении эффекты применяются к полному разрешению изображения.</p>
        
        <h3 style="color: #0e639c;">Интерфейс</h3>
        <ul>
            <li><b>Левая панель:</b> Просмотр оригинального и обработанного изображения</li>
            <li><b>Правая панель:</b> Выбор эффектов, настройка параметров, стек эффектов</li>
            <li><b>Верхняя панель:</b> Меню и инструменты</li>
            <li><b>Нижняя панель:</b> Статус-бар с информацией о размере, формате и времени обработки</li>
        </ul>
        
        <h3 style="color: #0e639c;">Масштабирование</h3>
        <p>В toolbar доступны три режима:</p>
        <ul>
            <li><b>Fit:</b> Автоматическое масштабирование под размер окна</li>
            <li><b>100%:</b> Реальный размер изображения</li>
            <li><b>200%:</b> Увеличение в 2 раза</li>
        </ul>
        
        <h3 style="color: #0e639c;">Стек эффектов</h3>
        <p>Эффекты применяются последовательно, порядок имеет значение!</p>
        <ul>
            <li><b>Чекбокс:</b> Включить/выключить эффект без удаления</li>
            <li><b>Перетаскивание:</b> Изменить порядок применения</li>
            <li><b>Кнопка "×":</b> Удалить эффект из стека</li>
        </ul>
        """
        
        widget = QWidget()
        layout = QVBoxLayout()
        text_widget = self.create_text_widget(content)
        layout.addWidget(text_widget)
        widget.setLayout(layout)
        return widget
    
    def create_effects_tab(self) -> QWidget:
        """Create effects instructions tab."""
        content = """
        <h2 style="color: #007acc;">Эффекты</h2>
        
        <h3 style="color: #0e639c;">Geometry (Геометрия)</h3>
        
        <h4>Shift Rows/Columns</h4>
        <p>Сдвигает строки или столбцы изображения с плавной случайностью.</p>
        <ul>
            <li><b>Direction:</b> rows (строки), columns (столбцы), both (оба)</li>
            <li><b>Max Shift:</b> Максимальный сдвиг в пикселях (0-1000)</li>
            <li><b>Smoothness:</b> Плавность изменения (0.0-1.0) - чем выше, тем плавнее</li>
            <li><b>Seed:</b> Зерно для генератора случайных чисел</li>
            <li><b>Wrap Mode:</b> wrap (заворачивание), reflect (отражение), clamp (закрепление)</li>
        </ul>
        
        <h4>Warp</h4>
        <p>Искажает изображение волнами или шумовым полем.</p>
        <ul>
            <li><b>Type:</b> wave (волны), noise (шум)</li>
            <li><b>Amount:</b> Сила смещения в пикселях (0.0-100.0)</li>
            <li><b>Scale:</b> Размер волн/шума - меньше = более частые волны</li>
            <li><b>Angle:</b> Угол направления волн (0-360°)</li>
            <li><b>Interpolation:</b> nearest (быстро), bilinear (баланс), bicubic (качественно)</li>
        </ul>
        
        <h4>Block Shuffle</h4>
        <p>Перемешивает мозаику блоков, сохраняя узнаваемость.</p>
        <ul>
            <li><b>Block Size:</b> Размер блока (8, 16, 32, 64, 128 пикселей)</li>
            <li><b>Shuffle Strength:</b> Доля блоков для перемешивания (0.0-1.0)</li>
            <li><b>Block Transform:</b> none, rotate, flip, jitter</li>
        </ul>
        
        <h4>Rotate/Flip</h4>
        <p>Поворачивает и/или отражает изображение.</p>
        <ul>
            <li><b>Rotation:</b> 0°, 90°, 180°, 270°</li>
            <li><b>Flip Horizontal/Vertical:</b> Отражение по осям</li>
        </ul>
        
        <h4>Crop</h4>
        <p>Обрезает изображение по заданным координатам.</p>
        <ul>
            <li><b>X, Y:</b> Начальные координаты</li>
            <li><b>Width, Height:</b> Размеры области</li>
            <li><b>Mode:</b> percent (проценты) или absolute (пиксели)</li>
        </ul>
        
        <h4>Scale</h4>
        <p>Изменяет размер изображения.</p>
        <ul>
            <li><b>Scale X/Y:</b> Масштаб в процентах (1-1000%)</li>
            <li><b>Interpolation:</b> Метод интерполяции (nearest, bilinear, bicubic, lanczos)</li>
        </ul>
        
        <h3 style="color: #0e639c;">Color (Цвет)</h3>
        
        <h4>HSV Adjust</h4>
        <p>Корректирует оттенок, насыщенность и яркость.</p>
        <ul>
            <li><b>Hue Shift:</b> Сдвиг оттенка (-180 до 180)</li>
            <li><b>Saturation:</b> Насыщенность (0.0-2.0) - 0 = чёрно-белое</li>
            <li><b>Value:</b> Яркость (0.0-2.0) - 0 = чёрное, >1 = осветление</li>
        </ul>
        
        <h4>RGB Curves</h4>
        <p>Корректирует контраст, гамму и экспозицию.</p>
        <ul>
            <li><b>Contrast:</b> Контрастность (-100 до 100)</li>
            <li><b>Gamma:</b> Гамма-коррекция (0.2-3.0) - <1 осветляет тени</li>
            <li><b>Exposure:</b> Экспозиция (-2.0 до 2.0) - отрицательные затемняют</li>
        </ul>
        
        <h4>Channel Shuffle</h4>
        <p>Переставляет каналы RGB и смешивает их.</p>
        <ul>
            <li><b>Mode:</b> rgb, rbg, grb, gbr, brg, bgr, mix</li>
            <li><b>Mix Amount:</b> Сила смешивания (0.0-1.0, только для mix)</li>
        </ul>
        
        <h4>Posterize</h4>
        <p>Уменьшает количество цветов (постеризация).</p>
        <ul>
            <li><b>Levels:</b> Количество уровней цвета (2-256)</li>
            <li><b>Dither:</b> Дизеринг для сглаживания переходов</li>
        </ul>
        
        <h3 style="color: #0e639c;">Detail (Детали)</h3>
        
        <h4>Grain</h4>
        <p>Добавляет зернистость (шум) к изображению.</p>
        <ul>
            <li><b>Amount:</b> Количество зерна (0.0-1.0)</li>
            <li><b>Size:</b> Размер зерна (1-5)</li>
            <li><b>Monochrome:</b> Монохромное зерно (одинаковое для всех каналов)</li>
        </ul>
        
        <h4>Sharpen/Blur</h4>
        <p>Увеличивает резкость или размывает изображение.</p>
        <ul>
            <li><b>Mode:</b> blur (размытие) или sharpen (резкость)</li>
            <li><b>Blur Sigma:</b> Сила размытия (0.0-10.0)</li>
            <li><b>Sharpen Amount:</b> Сила резкости (0.0-2.0)</li>
        </ul>
        """
        
        widget = QWidget()
        layout = QVBoxLayout()
        text_widget = self.create_text_widget(content)
        layout.addWidget(text_widget)
        widget.setLayout(layout)
        return widget
    
    def create_parameters_tab(self) -> QWidget:
        """Create parameters instructions tab."""
        content = """
        <h2 style="color: #007acc;">Типы параметров</h2>
        
        <h3 style="color: #0e639c;">SpinBox (Целые числа)</h3>
        <p>Используется для целочисленных значений (например, размеры, углы, seed).</p>
        <ul>
            <li>Используйте стрелки вверх/вниз для изменения значения</li>
            <li>Или введите значение напрямую</li>
            <li>Значение автоматически ограничивается допустимым диапазоном</li>
        </ul>
        
        <h3 style="color: #0e639c;">DoubleSpinBox (Дробные числа)</h3>
        <p>Используется для значений с десятичными дробями (например, проценты, коэффициенты).</p>
        <ul>
            <li>Используйте стрелки для изменения с шагом 0.1</li>
            <li>Или введите значение с десятичной точкой (например, 0.5)</li>
            <li>Точность: 2 знака после запятой</li>
        </ul>
        
        <h3 style="color: #0e639c;">ComboBox (Выбор из списка)</h3>
        <p>Используется для выбора из предопределённых опций.</p>
        <ul>
            <li>Нажмите на поле, чтобы открыть список</li>
            <li>Выберите нужную опцию</li>
            <li>Примеры: Direction (rows/columns/both), Wrap Mode, Interpolation</li>
        </ul>
        
        <h3 style="color: #0e639c;">CheckBox (Да/Нет)</h3>
        <p>Используется для включения/выключения опций.</p>
        <ul>
            <li>Установите галочку для включения</li>
            <li>Снимите галочку для выключения</li>
            <li>Примеры: Flip Horizontal, Dither, Monochrome</li>
        </ul>
        
        <h3 style="color: #0e639c;">Советы по настройке</h3>
        <ul>
            <li><b>Начните с малых значений:</b> Сначала попробуйте небольшие изменения</li>
            <li><b>Используйте Randomize:</b> Для быстрого поиска интересных комбинаций</li>
            <li><b>Экспериментируйте:</b> Многие эффекты дают неожиданные результаты</li>
            <li><b>Комбинируйте эффекты:</b> Порядок применения важен!</li>
            <li><b>Seed для воспроизводимости:</b> Зафиксируйте seed для повторения результата</li>
        </ul>
        """
        
        widget = QWidget()
        layout = QVBoxLayout()
        text_widget = self.create_text_widget(content)
        layout.addWidget(text_widget)
        widget.setLayout(layout)
        return widget
    
    def create_buttons_tab(self) -> QWidget:
        """Create buttons instructions tab."""
        content = """
        <h2 style="color: #007acc;">Кнопки и действия</h2>
        
        <h3 style="color: #0e639c;">Toolbar (Верхняя панель)</h3>
        
        <h4>Open</h4>
        <p>Открыть изображение. Горячая клавиша: <code>Ctrl+O</code></p>
        
        <h4>Save</h4>
        <p>Сохранить обработанное изображение. Горячая клавиша: <code>Ctrl+S</code></p>
        
        <h4>Reset</h4>
        <p>Сбросить все эффекты и вернуться к исходному изображению.</p>
        
        <h4>Undo</h4>
        <p>Отменить последнее действие. Горячая клавиша: <code>Ctrl+Z</code></p>
        
        <h4>Redo</h4>
        <p>Повторить отменённое действие. Горячая клавиша: <code>Ctrl+Y</code></p>
        
        <h4>Zoom</h4>
        <p>Выпадающий список для выбора масштаба: Fit, 100%, 200%</p>
        
        <h3 style="color: #0e639c;">Панель эффектов</h3>
        
        <h4>Кнопки эффектов</h4>
        <p>Нажмите на название эффекта в списке, чтобы выбрать его для настройки.</p>
        
        <h4>Randomize</h4>
        <p>Случайно изменяет все параметры текущего эффекта в безопасных диапазонах. 
        Используется для экспериментов и поиска интересных комбинаций.</p>
        
        <h4>Apply</h4>
        <p>Применяет эффект с текущими параметрами и добавляет его в стек эффектов. 
        Эффект сразу отображается в предпросмотре.</p>
        
        <h3 style="color: #0e639c;">Стек эффектов</h3>
        
        <h4>Чекбокс</h4>
        <p>Включить/выключить эффект без удаления из стека. 
        Полезно для сравнения результатов с эффектом и без него.</p>
        
        <h4>Кнопка "×"</h4>
        <p>Удалить эффект из стека. Эффект полностью удаляется, но можно отменить через Undo.</p>
        
        <h4>Clear All</h4>
        <p>Очистить весь стек эффектов. Все эффекты удаляются, изображение возвращается к исходному виду.</p>
        
        <h4>Перетаскивание</h4>
        <p>Перетащите эффект мышью, чтобы изменить его порядок в стеке. 
        Порядок эффектов имеет значение для конечного результата!</p>
        
        <h3 style="color: #0e639c;">Меню</h3>
        
        <h4>File → Open</h4>
        <p>Открыть изображение (<code>Ctrl+O</code>)</p>
        
        <h4>File → Save As</h4>
        <p>Сохранить изображение (<code>Ctrl+S</code>)</p>
        
        <h4>File → Save Preset</h4>
        <p>Сохранить текущий стек эффектов и их параметры в JSON файл.</p>
        
        <h4>File → Load Preset</h4>
        <p>Загрузить пресет из JSON файла. Эффекты применятся автоматически.</p>
        
        <h4>File → Random Preset</h4>
        <p>Применить случайный набор из 1-3 эффектов с случайными параметрами.</p>
        
        <h4>File → Exit</h4>
        <p>Выход из приложения (<code>Alt+F4</code>)</p>
        
        <h4>Edit → Undo</h4>
        <p>Отменить действие (<code>Ctrl+Z</code>)</p>
        
        <h4>Edit → Redo</h4>
        <p>Повторить действие (<code>Ctrl+Y</code>)</p>
        
        <h4>Edit → Reset</h4>
        <p>Сбросить все эффекты</p>
        
        <h4>View → Show Logs</h4>
        <p>Показать панель с логами приложения</p>
        """
        
        widget = QWidget()
        layout = QVBoxLayout()
        text_widget = self.create_text_widget(content)
        layout.addWidget(text_widget)
        widget.setLayout(layout)
        return widget

