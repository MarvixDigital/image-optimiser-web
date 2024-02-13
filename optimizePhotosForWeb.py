import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout,
                             QFileDialog, QLabel, QTextEdit, QCheckBox,
                             QMessageBox, QLineEdit, QFormLayout, QGroupBox, QSlider, QHBoxLayout)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PIL import Image

class ImageOptimizerThread(QThread):
    update_progress = pyqtSignal(str)

    def __init__(self, files, output_folder, export_formats, sizes, custom_size, custom_suffix, quality):
        super().__init__()
        self.files = files
        self.output_folder = output_folder
        self.export_formats = export_formats
        self.sizes = sizes
        self.custom_size = custom_size
        self.custom_suffix = custom_suffix
        self.quality = quality

    def run(self):
        if self.custom_size and self.custom_suffix:
            try:
                self.sizes.append({"width": int(self.custom_size), "suffix": self.custom_suffix})
            except ValueError:
                self.update_progress.emit(f"Error: Custom width '{self.custom_size}' is not valid.")
                return

        for file in self.files:
            filename, ext = os.path.splitext(os.path.basename(file))
            for size in self.sizes:
                with Image.open(file) as img:
                    w_percent = (size["width"] / float(img.size[0]))
                    h_size = int((float(img.size[1]) * float(w_percent)))
                    img_resized = img.resize((size["width"], h_size), Image.ANTIALIAS)
                    for format in self.export_formats:
                        output_filename = f"{filename}-{size['suffix']}.{format}"
                        output_path = os.path.join(self.output_folder, output_filename)
                        img_resized.save(output_path, format.upper(), quality=self.quality)
                        self.update_progress.emit(f"Saved: {output_filename}")

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Image Optimizer'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(10, 10, 640, 480)

        layout = QVBoxLayout()

        self.label = QLabel('Select images and output folder, then choose formats, sizes, quality, and start optimization.')
        layout.addWidget(self.label)

        btn_select_files = QPushButton('Select Images')
        btn_select_files.clicked.connect(self.select_files)
        layout.addWidget(btn_select_files)

        self.btn_select_output_folder = QPushButton('Select Output Folder')
        self.btn_select_output_folder.clicked.connect(self.select_output_folder)
        layout.addWidget(self.btn_select_output_folder)

        # Formats selection
        self.format_group = QGroupBox("Formats")
        format_layout = QVBoxLayout()
        self.format_options = {
            'jpeg': QCheckBox('JPEG'),
            'webp': QCheckBox('WebP'),
            'png': QCheckBox('PNG')
        }
        for format_option in self.format_options.values():
            format_option.setChecked(True)
            format_layout.addWidget(format_option)
        self.format_group.setLayout(format_layout)
        layout.addWidget(self.format_group)

        # Sizes selection
        self.size_group = QGroupBox("Sizes")
        size_layout = QVBoxLayout()
        self.size_options = {
            'small': QCheckBox('Small (320px width)'),
            'medium': QCheckBox('Medium (480px width)'),
            'large': QCheckBox('Large (800px width)'),
            'extra-large': QCheckBox('Extra Large (1200px width)'),
            'cover': QCheckBox('Cover (2000px width)'),
        }
        for size_option in self.size_options.values():
            size_option.setChecked(True)
            size_layout.addWidget(size_option)
        self.size_group.setLayout(size_layout)
        layout.addWidget(self.size_group)

        # Custom size and suffix
        self.custom_size_group = QGroupBox("Custom Size")
        custom_size_layout = QFormLayout()
        self.custom_width_input = QLineEdit()
        self.custom_suffix_input = QLineEdit()
        custom_size_layout.addRow("Custom width (px):", self.custom_width_input)
        custom_size_layout.addRow("Custom suffix:", self.custom_suffix_input)
        self.custom_size_group.setLayout(custom_size_layout)
        layout.addWidget(self.custom_size_group)

        # Quality slider
        self.quality_group = QGroupBox("Quality")
        quality_layout = QHBoxLayout()
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setMinimum(1)
        self.quality_slider.setMaximum(100)
        self.quality_slider.setValue(90)  # Default value
        self.quality_slider.setTickPosition(QSlider.TicksBelow)
        self.quality_slider.setTickInterval(10)
        quality_layout.addWidget(self.quality_slider)
        self.quality_label = QLabel('90')
        self.quality_slider.valueChanged.connect(lambda: self.quality_label.setText(str(self.quality_slider.value())))
        quality_layout.addWidget(self.quality_label)
        self.quality_group.setLayout(quality_layout)
        layout.addWidget(self.quality_group)

        self.progress_text = QTextEdit()
        self.progress_text.setReadOnly(True)
        layout.addWidget(self.progress_text)

        btn_start_optimization = QPushButton('Start Optimization')
        btn_start_optimization.clicked.connect(self.start_optimization)
        layout.addWidget(btn_start_optimization)

        self.setLayout(layout)

    def select_files(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", "Image Files (*.jpg *.jpeg *.png)", options=options)
        if files:
            self.files = files
            self.label.setText(f"{len(files)} files selected")

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_folder = folder
            self.btn_select_output_folder.setText(folder)

    def start_optimization(self):
        selected_formats = [fmt for fmt, cb in self.format_options.items() if cb.isChecked()]
        selected_sizes = [{"width": size[0], "suffix": size[1]} for size, cb in zip([(320, 'small'), (480, 'medium'), (800, 'large'), (1200, 'extra-large'), (2000, 'cover')], self.size_options.values()) if cb.isChecked()]
        custom_size = self.custom_width_input.text().strip()
        custom_suffix = self.custom_suffix_input.text().strip()
        quality = self.quality_slider.value()

        if not self.files or not self.output_folder or not selected_formats or not selected_sizes and not (custom_size and custom_suffix):
            QMessageBox.warning(self, "Warning", "Please select images, an output folder, at least one format, and at least one size.")
            return

        self.progress_text.clear()
        self.thread = ImageOptimizerThread(self.files, self.output_folder, selected_formats, selected_sizes, custom_size, custom_suffix, quality)
        self.thread.update_progress.connect(self.update_progress)
        self.thread.start()

    def update_progress(self, message):
        self.progress_text.append(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
