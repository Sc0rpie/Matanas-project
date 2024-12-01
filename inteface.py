import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel, QFileDialog, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

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
            # Load image and convert to grayscale
            img = Image.open(file_name).convert('L')  # 'L' mode converts to grayscale
            
            # Convert image to a numpy array
            img_array = np.array(img)

            pixmap = QPixmap(file_name)
            pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio)  # Resize image to fit label
            self.image_label1.setPixmap(pixmap)

            # Generate and display the graph
            self.display_graph(img_array, self.graph1_label)

    def upload_image2(self):
        # Open file dialog to select an image
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image 2", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff)", options=options)
        
        if file_name:
            # Load image and convert to grayscale
            img = Image.open(file_name).convert('L')
            img_array = np.array(img)

            # Display the image in the QLabel
            pixmap = QPixmap(file_name)
            pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio)
            self.image_label2.setPixmap(pixmap)

            # Generate and display the graph
            self.display_graph(img_array, self.graph2_label)

    def display_graph(self, img_array, graph_label):
        # # Generate the graph for the grayscale image data
        # fig, ax = plt.subplots()
        # ax.hist(img_array.flatten(), bins=256, range=(0, 256), color='gray')  # Histogram of pixel intensities
        # ax.set_title('Grayscale Pixel Intensity Distribution')
        # ax.set_xlabel('Pixel Intensity')
        # ax.set_ylabel('Frequency')

        # # Convert the matplotlib figure to a QPixmap
        # buf = BytesIO()
        # fig.savefig(buf, format='png')
        # buf.seek(0)
        # img = QPixmap()
        # img.loadFromData(buf.getvalue())
        # buf.close()
        
          # Generate the graph for each pixel's intensity
        pixel_indices = np.arange(img_array.size)  # Create an array of pixel indices
        pixel_values = img_array.flatten()         # Flatten the image array to get pixel intensities

        fig, ax = plt.subplots(figsize=(45, 5))  # Adjust this line as needed
        ax.plot(pixel_indices, pixel_values, color='gray', marker='o', markersize=1)  # Plot each pixel intensity

        ax.set_title('Pixel Intensities')
        ax.set_xlabel('Pixel Index')
        ax.set_ylabel('Pixel Intensity (0-255)')
        ax.set_xlim(0, img_array.size)  # Set x limits to the number of pixels
        ax.set_ylim(0, 255)              # Set y limits from 0 to 255

        plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.1)  # Adjust margins as needed
        # Convert the matplotlib figure to a QPixmap
        buf = BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        img = QPixmap()
        img.loadFromData(buf.getvalue())
        buf.close()
        

        # Set the graph image in the QLabel
        graph_label.setPixmap(img.scaled(2200, 300, Qt.KeepAspectRatio))
# Main function to run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageUploaderApp()
    window.show()
    sys.exit(app.exec_())