import os
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QLabel, QPushButton, QListWidget, QComboBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter, ImageEnhance


# Create the application instance
app = QApplication([])
window = QWidget()
window.setWindowTitle('Photo Editor')
window.resize(900, 700)

# Create the widgets
button_folder = QPushButton('Open Folder')
file_list = QListWidget()

btn_left = QPushButton('Left')
btn_right = QPushButton('Right')
mirror = QPushButton('Mirror')
sharpen = QPushButton('Sharpen')
blur = QPushButton('Blur')
resize = QPushButton('Resize')
crop = QPushButton('Crop')
brightness = QPushButton('Brightness')
contrast = QPushButton('Contrast')
saturation = QPushButton('Saturation')
hue = QPushButton('Hue')
gamma = QPushButton('Gamma')
exposure = QPushButton('Exposure')
highlight = QPushButton('Highlight')
shadow = QPushButton('Shadow')
noise = QPushButton('Noise')
sepia = QPushButton('Sepia')
grayscale = QPushButton('Grayscale')
invert = QPushButton('Invert')
auto_contrast = QPushButton('Auto Contrast')
auto_color = QPushButton('Auto Color')

# Dropdown menu
filter_list = QComboBox()
filter_list.addItem('Original')
filter_list.addItem('Mirror')
filter_list.addItem('Sharpen')
filter_list.addItem('Blur')
filter_list.addItem('Rotate')
filter_list.addItem('Resize')
filter_list.addItem('Crop')
filter_list.addItem('Brightness')
filter_list.addItem('Contrast')
filter_list.addItem('Saturation')
filter_list.addItem('Hue')
filter_list.addItem('Gamma')
filter_list.addItem('Exposure')
filter_list.addItem('Highlight')
filter_list.addItem('Shadow')
filter_list.addItem('Noise')
filter_list.addItem('Sepia')
filter_list.addItem('Grayscale')
filter_list.addItem('Invert')
filter_list.addItem('Auto Contrast')
filter_list.addItem('Auto Color')

picture_box = QLabel('Picture')

# Create App Design
layout = QHBoxLayout()

col1 = QVBoxLayout()
col2 = QVBoxLayout()

col1.addWidget(button_folder)
col1.addWidget(file_list)
col1.addWidget(filter_list)
col1.addWidget(btn_left)
col1.addWidget(btn_right)
col1.addWidget(mirror)
col1.addWidget(sharpen)
col1.addWidget(blur)
col1.addWidget(resize)
col1.addWidget(crop)
col1.addWidget(grayscale)



col2.addWidget(picture_box)


layout.addLayout(col1, 20)
layout.addLayout(col2, 80)

window.setLayout(layout)



# All App functionality

working_directory = ""

# Filter files and extensions
def filter_files(files, extensions):
    results = []
    for file in files:
        for ext in extensions:
            if file.endswith(ext):
                results.append(file)
    return results

# Choose current directory
def choose_directory():
    global working_directory
    working_directory = QFileDialog.getExistingDirectory(window, 'Open Directory')
    files = os.listdir(working_directory)
    images = filter_files(files, ['.png', '.jpg', '.jpeg', ".svg"])
    file_list.clear()
    for filename in images: # Iterate over the list of image filenames
        file_list.addItem(filename)
    file_list.addItems(images)

# Image Editor Class
class Editor():
    def __init__(self):
        self.image = None
        self.original = None
        self.filename = None
        self.save_directory = "edits/"

    def open_image(self, filename):
        self.filename = filename
        fullname = os.path.join(working_directory, self.filename)
        self.image = Image.open(fullname)
        self.original = self.image.copy()
    
    def save_image(self):
        path = os.path.join(working_directory, self.save_directory)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)

        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)
    
    def show_image(self, path):
        picture_box.hide()
        image = QPixmap(path)
        w, h = picture_box.width(), picture_box.height()
        image = image.scaled(w, h, Qt.KeepAspectRatio)
        picture_box.setPixmap(image)
        picture_box.show()
    
    # button functions
    def left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.save_image()
        image_path = os.path.join(working_directory, self.save_directory, self.filename)
        self.show_image(image_path)  

    def right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.save_image()
        image_path = os.path.join(working_directory, self.save_directory, self.filename)
        self.show_image(image_path)

    def mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.save_image()
        image_path = os.path.join(working_directory, self.save_directory, self.filename)
        self.show_image(image_path)

    def sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.save_image()
        image_path = os.path.join(working_directory, self.save_directory, self.filename)
        self.show_image(image_path)

    def blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.save_image()
        image_path = os.path.join(working_directory, self.save_directory, self.filename)
        self.show_image(image_path)    
    
    def resize(self):
        self.image = self.image.resize((300, 300))
        self.save_image()
        image_path = os.path.join(working_directory, self.save_directory, self.filename)
        self.show_image(image_path)

    def crop(self):
        self.image = self.image.crop((100, 100, 400, 400))
        self.save_image()
        image_path = os.path.join(working_directory, self.save_directory, self.filename)
        self.show_image(image_path)

    def brightness(self):
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(2)
        self.save_image()
        image_path = os.path.join(working_directory, self.save_directory, self.filename)
        self.show_image(image_path)

    def contrast(self):
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(2)
        self.save_image()
        image_path = os.path.join(working_directory, self.save_directory, self.filename)
        self.show_image(image_path)

    def grayscale(self):
        self.image = self.image.convert('L')
        self.save_image()
        image_path = os.path.join(working_directory, self.save_directory, self.filename)
        self.show_image(image_path)

    # Dropdown menu lambda functions
    def apply_filter(self, filter_name):
        if filter_name == 'Original':
            self.image = self.original.copy()
        else:
            filter_mapping = {
                "Left": lambda image: image.transpose(Image.ROTATE_90),
                "Right": lambda image: image.transpose(Image.ROTATE_270),
                "Mirror": lambda image: image.transpose(Image.FLIP_LEFT_RIGHT),
                "Sharpen": lambda image: image.filter(ImageFilter.SHARPEN),
                "Blur": lambda image: image.filter(ImageFilter.BLUR),
                "Resize": lambda image: image.resize((300, 300)),
                "Crop": lambda image: image.crop((100, 100, 400, 400)),
                "Brightness": lambda image: ImageEnhance.Brightness(image).enhance(2),
                "Contrast": lambda image: ImageEnhance.Contrast(image).enhance(2),
                "Grayscale": lambda image: image.convert('L')
            }
            filter_function = filter_mapping.get(filter_name)
            if filter_function:
                self.image = filter_function(self.image)
                self.save_image()
                image_path = os.path.join(working_directory, self.save_directory, self.filename)
                self.show_image(image_path)
            pass

        self.save_image()
        image_path = os.path.join(working_directory, self.save_directory, self.filename)
        self.show_image(image_path)

def handle_filter(filter_name):
    filter_name = filter_list.currentText()
    if file_list.currentRow() >= 0:
        filename = file_list.currentItem().text()
        main.open_image(filename)
        main.apply_filter(filter_name)

def displayImage():
    if file_list.currentRow() >= 0:
        filename = file_list.currentItem().text()
        main.open_image(filename)
        main.show_image(os.path.join(working_directory, filename))

main = Editor()

button_folder.clicked.connect(choose_directory)
file_list.currentRowChanged.connect(displayImage)
filter_list.currentTextChanged.connect(handle_filter)

btn_left.clicked.connect(main.left)
btn_right.clicked.connect(main.right)
mirror.clicked.connect(main.mirror)
sharpen.clicked.connect(main.sharpen)
blur.clicked.connect(main.blur)
resize.clicked.connect(main.resize)
crop.clicked.connect(main.crop)
brightness.clicked.connect(main.brightness)
contrast.clicked.connect(main.contrast)
grayscale.clicked.connect(main.grayscale)



window.show()
app.exec_()
