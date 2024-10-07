import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton, QLabel, QFileDialog, QVBoxLayout
)
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
        self.setGeometry(100, 100, 1600, 900)  # Increased size for three graphs

        # Create a grid layout
        layout = QGridLayout()
        
        # Section 1: Upload Image 1
        self.upload_btn1 = QPushButton('Upload Image 1')
        self.upload_btn1.clicked.connect(self.upload_image1)
        layout.addWidget(self.upload_btn1, 0, 0)

        self.image_label1 = QLabel("No Image 1")
        self.image_label1.setAlignment(Qt.AlignCenter)
        self.image_label1.setFixedSize(400, 300)  # Fixed size for consistency
        layout.addWidget(self.image_label1, 1, 0)
        
        # Section 2: Graph for Image 1
        self.graph1_label = QLabel("Graph 1 goes here")
        self.graph1_label.setAlignment(Qt.AlignCenter)
        self.graph1_label.setFixedSize(800, 300)
        layout.addWidget(self.graph1_label, 0, 1, 2, 1)  # Span across 2 rows
        
        # Section 3: Upload Image 2
        self.upload_btn2 = QPushButton('Upload Image 2')
        self.upload_btn2.clicked.connect(self.upload_image2)
        layout.addWidget(self.upload_btn2, 2, 0)

        self.image_label2 = QLabel("No Image 2")
        self.image_label2.setAlignment(Qt.AlignCenter)
        self.image_label2.setFixedSize(400, 300)
        layout.addWidget(self.image_label2, 3, 0)
        
        # Section 4: Graph for Image 2
        self.graph2_label = QLabel("Graph 2 goes here")
        self.graph2_label.setAlignment(Qt.AlignCenter)
        self.graph2_label.setFixedSize(800, 300)
        layout.addWidget(self.graph2_label, 2, 1, 2, 1)  # Span across 2 rows
        
        # Section 5: Graph for Comparison
        self.comparison_graph_label = QLabel("Comparison Graph goes here")
        self.comparison_graph_label.setAlignment(Qt.AlignCenter)
        self.comparison_graph_label.setFixedSize(1200, 300)
        layout.addWidget(self.comparison_graph_label, 4, 0, 1, 2)  # Span across 2 columns
        
        # Section 6: Display difference between graphs
        self.difference_label = QLabel("Max Difference: N/A")
        self.difference_label.setAlignment(Qt.AlignCenter)
        self.difference_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.difference_label, 5, 0, 1, 2)  # Span across two columns
        
        # Set the layout
        self.setLayout(layout)
        
        # Attributes to store the pixel intensity arrays
        self.image1_array = None
        self.image2_array = None

    def upload_image1(self):
        # Open file dialog to select an image
        self.image1_array = None  # Reset the array before uploading a new image
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Image 1", "", 
            "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff)", options=options
        )
        
        if file_name:
            try:
                # Load image and convert to grayscale
                img = Image.open(file_name).convert('L')  # 'L' mode converts to grayscale
                
                # Convert image to a numpy array with signed integers to prevent underflow
                self.image1_array = np.array(img, dtype=np.int16)

                pixmap = QPixmap(file_name)
                pixmap = pixmap.scaled(self.image_label1.size(), Qt.KeepAspectRatio)  # Resize image to fit label
                self.image_label1.setPixmap(pixmap)

                # Generate and display the graph for Image 1
                self.display_graph()

                # Calculate and update the difference if both images are loaded
                self.update_difference()
            except Exception as e:
                self.difference_label.setText(f"Error loading Image 1: {e}")

    def upload_image2(self):
        self.image2_array = None  # Reset the array before uploading a new image
        # Open file dialog to select an image
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Image 2", "", 
            "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff)", options=options
        )
        
        if file_name:
            try:
                # Load image and convert to grayscale
                img = Image.open(file_name).convert('L')
                self.image2_array = np.array(img, dtype=np.int16)  # Use signed type to prevent overflow

                # Display the image in the QLabel
                pixmap = QPixmap(file_name)
                pixmap = pixmap.scaled(self.image_label2.size(), Qt.KeepAspectRatio)
                self.image_label2.setPixmap(pixmap)

                # Generate and display the graph for Image 2
                self.display_graph()

                # Calculate and update the difference if both images are loaded
                self.update_difference()
            except Exception as e:
                self.difference_label.setText(f"Error loading Image 2: {e}")

    def display_graph(self):
        # Generate graphs for each image separately
        if self.image1_array is not None:
            # Generate the graph for Image 1
            self.generate_individual_graph(self.image1_array, self.graph1_label, title='Image 1 Pixel Intensities')

        if self.image2_array is not None:
            # Generate the graph for Image 2
            self.generate_individual_graph(self.image2_array, self.graph2_label, title='Image 2 Pixel Intensities')

        # If both images are uploaded, generate comparison graph
        if self.image1_array is not None and self.image2_array is not None:
            self.generate_comparison_graph()

    def generate_individual_graph(self, img_array, graph_label, title='Pixel Intensities'):
        # Flatten the image array to get pixel intensities
        pixel_values = img_array.flatten()
        pixel_indices = np.arange(pixel_values.size)

        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot(pixel_indices, pixel_values, color='gray')
        ax.set_title(title)
        ax.set_xlabel('Pixel Index')
        ax.set_ylabel('Pixel Intensity (0-255)')
        ax.set_xlim(0, pixel_values.size)
        ax.set_ylim(0, 255)
        plt.tight_layout()

        # Convert the matplotlib figure to a QPixmap
        buf = BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        img = QPixmap()
        img.loadFromData(buf.getvalue())
        buf.close()

        # Set the graph image in the QLabel
        graph_label.setPixmap(img.scaled(graph_label.size(), Qt.KeepAspectRatio))
        plt.close(fig)  # Close the figure to free memory

    def generate_comparison_graph(self):
        # Ensure both images have the same shape
        if self.image1_array.shape != self.image2_array.shape:
            # Resize the second image to match the first image's shape
            img2_resized = Image.fromarray(self.image2_array.astype(np.uint8)).resize(
                self.image1_array.shape[::-1], Image.LANCZOS
            )
            img2_array_resized = np.array(img2_resized, dtype=np.int16)
        else:
            img2_array_resized = self.image2_array

        # Compute the absolute differences between corresponding pixels
        differences = np.abs(self.image1_array - img2_array_resized)

        # **DEBUGGING OUTPUT: Print the entire differences array**
        print("Differences Array:")
        print(differences)

        # Flatten the arrays for plotting
        pixel_values1 = self.image1_array.flatten()
        pixel_values2 = img2_array_resized.flatten()
        diff_values = differences.flatten()
        pixel_indices = np.arange(pixel_values1.size)

        # Create the comparison plot
        fig, ax = plt.subplots(figsize=(12, 4))

        # Plot pixel intensities for both images
        ax.plot(pixel_indices, pixel_values1, color='blue', label='Image 1')
        ax.plot(pixel_indices, pixel_values2, color='red', label='Image 2')

        # Plot the absolute differences
        ax.plot(pixel_indices, diff_values, color='green', label='Absolute Difference')

        # Find the maximum difference
        max_difference = np.max(differences)
        max_diff_indices = np.argwhere(differences == max_difference)

        # **Correct Index Mapping: Convert 2D indices to 1D**
        # Take the first occurrence
        max_diff_position = max_diff_indices[0]
        max_diff_index = np.ravel_multi_index(max_diff_position, self.image1_array.shape)

        # Highlight the point of maximum difference
        ax.plot(max_diff_index, pixel_values1[max_diff_index], 'go', label='Max Diff Point Image 1')
        ax.plot(max_diff_index, pixel_values2[max_diff_index], 'mo', label='Max Diff Point Image 2')
        ax.plot(max_diff_index, diff_values[max_diff_index], 'yo', label='Max Diff Value')

        # Annotate the maximum difference
        ax.annotate(
            f'Max Diff: {max_difference}',
            xy=(max_diff_index, diff_values[max_diff_index]),
            xytext=(max_diff_index, diff_values[max_diff_index] + 20),
            arrowprops=dict(facecolor='yellow', shrink=0.05),
            fontsize=9,
            ha='center'
        )

        ax.set_title('Pixel Intensities Comparison')
        ax.set_xlabel('Pixel Index')
        ax.set_ylabel('Pixel Intensity / Difference (0-255)')
        ax.set_xlim(0, pixel_values1.size)
        ax.set_ylim(0, 255)
        ax.legend()

        plt.tight_layout()

        # Convert the matplotlib figure to a QPixmap
        buf = BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        img = QPixmap()
        img.loadFromData(buf.getvalue())
        buf.close()

        # Set the comparison graph image in the QLabel
        self.comparison_graph_label.setPixmap(img.scaled(self.comparison_graph_label.size(), Qt.KeepAspectRatio))
        plt.close(fig)  # Close the figure to free memory

        # Update the difference label
        self.difference_label.setText(f"Max Difference: {max_difference} at Pixel Index: {max_diff_index}")

    def update_difference(self):
        # This method is now handled within generate_comparison_graph
        pass

# Main function to run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageUploaderApp()
    window.show()
    sys.exit(app.exec_())