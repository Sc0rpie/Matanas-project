import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel, QFileDialog, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image
import matplotlib.pyplot as plt

class ImageUploaderApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set up the window
        self.setWindowTitle("Image Uploader App")
        self.setGeometry(100, 100, 800, 600)  # Size of the window

        # Create a grid layout
        layout = QGridLayout()
        
        # Section 1: Upload Image 1
        self.upload_btn1 = QPushButton('Upload Image 1')
        self.upload_btn1.clicked.connect(self.upload_image1)
        layout.addWidget(self.upload_btn1, 0, 0)

        self.image_label1 = QLabel("No Image 1")
        self.image_label1.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label1, 1, 0)
        
        # Section 2: Placeholder for Graph 1
        self.graph1_label = QLabel("Graph 1 goes here")
        self.graph1_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.graph1_label, 0, 1, 2, 1)  # Span across 2 rows
        
        # Section 3: Upload Image 2
        self.upload_btn2 = QPushButton('Upload Image 2')
        self.upload_btn2.clicked.connect(self.upload_image2)
        layout.addWidget(self.upload_btn2, 2, 0)

        self.image_label2 = QLabel("No Image 2")
        self.image_label2.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label2, 3, 0)
        
        # Section 4: Placeholder for Graph 2
        self.graph2_label = QLabel("Graph 2 goes here")
        self.graph2_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.graph2_label, 2, 1, 2, 1)  # Span across 2 rows
        
        # Set the layout
        self.setLayout(layout)

    def upload_image1(self):
        # Open file dialog to select an image
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image 1", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff)", options=options)
        
        if file_name:
            pixmap = QPixmap(file_name)
            pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio)  # Resize image to fit label
            self.image_label1.setPixmap(pixmap)
    
    def upload_image2(self):
        # Open file dialog to select an image
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image 2", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff)", options=options)
        
        if file_name:
            pixmap = QPixmap(file_name)
            pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio)  # Resize image to fit label
            self.image_label2.setPixmap(pixmap)

# Main function to run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageUploaderApp()
    window.show()
    sys.exit(app.exec_())