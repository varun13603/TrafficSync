from tkinter import messagebox, filedialog, simpledialog, Tk, Label, Button
import cv2
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from CannyEdgeDetector import CannyEdgeDetector

class TrafficControlSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Density Based Smart Traffic Control System")
        self.root.geometry("600x400")

        self.filename = ""
        self.refrence_pixels = 0
        self.sample_pixels = 0

        self.font = ('Arial', 14)

        self.title = Label(root, text='Density Based Smart Traffic Control System', font=(self.font[0], 20, 'bold'), bg='lightblue')
        self.title.pack(pady=10)

        self.upload_button = Button(root, text="Upload Traffic Image", command=self.upload_traffic_image, font=self.font, bg='orange', fg='white')
        self.upload_button.pack()

        self.pathlabel = Label(root, text="Selected Image Path: ", font=self.font, bg='lightgreen')
        self.pathlabel.pack(pady=5)

    def upload_traffic_image(self):
        option = messagebox.askquestion("Choose Option", "Do you want to upload an image file?")
        if option == 'yes':
            self.filename = filedialog.askopenfilename(initialdir="images")
            self.pathlabel.config(text=self.filename)
            self.process_image()
        else:
            self.capture_from_camera()

    def capture_from_camera(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if ret:
            cv2.imwrite("captured_image.png", frame)
            self.filename = "captured_image.png"
            self.pathlabel.config(text=self.filename)
            self.process_image()
        else:
            messagebox.showerror("Error", "Failed to capture image from camera.")

    def process_image(self):
        try:
            img = mpimg.imread(self.filename)
            img = self.rgb2gray(img)
            edge_detector = CannyEdgeDetector([img], sigma=1.4, kernel_size=5, lowthreshold=0.09, highthreshold=0.20, weak_pixel=100)
            edges = edge_detector.detect()
            self.visualize([img, edges[0]])
            self.calculate_pixel_count()
            self.calculate_time_allocation()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def rgb2gray(self, rgb):
        return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

    def visualize(self, imgs):
        plt.figure(figsize=(10, 5))
        for i, img in enumerate(imgs):
            plt.subplot(1, 2, i+1)
            if i == 0:
                plt.title('Original Image')
            else:
                plt.title('Edge Detected Image')
            plt.imshow(img, cmap='gray')
        plt.show()

    def calculate_pixel_count(self):
    # Load reference image (assuming it's already loaded)
        ref_img = cv2.imread('gray/refrence.png', cv2.IMREAD_GRAYSCALE)
        self.refrence_pixels = np.sum(ref_img == 255)

        img = cv2.imread(self.filename, cv2.IMREAD_GRAYSCALE)
        # Check if grayscale (optional)
        if img.ndim == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.sample_pixels = np.sum(img == 255)

        messagebox.showinfo("Pixel Counts", f"Total Sample White Pixels Count: {self.sample_pixels}\nTotal Reference White Pixels Count: {self.refrence_pixels}")


    def calculate_time_allocation(self):
        print(self.sample_pixels)
        print(self.refrence_pixels)
        avg = (self.sample_pixels / self.refrence_pixels) * 100
        if avg >= 100:
            message = "Traffic is very high. Allocation green signal time: 60 secs"
        elif avg > 80:
            message = "Traffic is high. Allocation green signal time: 50 secs"
        elif avg > 60:
            message = "Traffic is moderate. Allocation green signal time: 40 secs"
        elif avg > 40:
            message = "Traffic is low. Allocation green signal time: 30 secs"
        else:
            message = "Traffic is very low. Allocation green signal time: 10 secs"
        messagebox.showinfo("Green Signal Allocation Time", message)

root = Tk()
app = TrafficControlSystem(root)
root.mainloop()
