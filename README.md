# Image Optimizer

## Introduction
Image Optimizer is a PyQt5-based GUI application designed to help users easily optimize images for web and storage purposes. It allows for resizing images into multiple predefined sizes, applying custom sizes, selecting various export formats, and adjusting the quality of the output images.

## Features
- **Multiple Export Formats**: Supports exporting images in JPEG, WebP, and PNG formats.
- **Predefined and Custom Sizes**: Optimize images to predefined sizes or specify a custom size and suffix.
- **Quality Adjustment**: Fine-tune the quality of the exported images with a simple slider.
- **Batch Processing**: Optimize multiple images at once for efficient workflow.

## Installation

### Prerequisites
- Python 3.6 or higher
- PyQt5
- Pillow

## Setup

### Prerequisites
- Python 3.6 or higher
- PyQt5
- Pillow

### Installation
1. Clone the repository to your local machine:
git clone https://github.com/yourusername/image-optimizer.git

2. Navigate to the cloned directory:
cd image-optimizer

3. Install the required Python packages:
pip install -r requirements.txt

### Building Executable Files

#### For Windows
To create an executable for Windows, you can use PyInstaller. If PyInstaller is not already installed, you can install it using pip:
pip install pyinstaller

Then, build the executable with the following command:
pyinstaller --onefile --windowed optimizePhotosForWeb.py

This command tells PyInstaller to bundle `optimizePhotosForWeb.py` into a single executable file (`--onefile`) without a console window (`--windowed`). The executable will be located in the `dist` directory.

#### For macOS
Building an executable for macOS is similar, but you might want to specify an icon for the application. First, ensure PyInstaller is installed:
pip install pyinstaller

Then, use PyInstaller to build the macOS application:
pyinstaller --onefile --windowed optimizePhotosForWeb.py

For macOS, if you have an icon file (e.g., `icon.icns`), you can include it with the `--icon` option:
pyinstaller --onefile --windowed --icon=icon.icns optimizePhotosForWeb.py

The application will be created in the `dist` directory.

## Usage
To start the application, if not using an executable, run:
python optimizePhotosForWeb.py

For executables, simply launch the created executable file from the `dist` directory.
