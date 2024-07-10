from tkinter import messagebox, Tk, Label, Button, filedialog
import cv2
import matplotlib.image as mpimg
import numpy as np
from CannyEdgeDetector import *
import matplotlib.pyplot as plt

main = Tk()
main.title("Density Based Smart Traffic Control System")
main.geometry("800x600")

filename = ""
refrence_pixels = 0
sample_pixels = 0

def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray

def visualize(imgs):
    plt.figure(figsize=(8, 6))
    for i, img in enumerate(imgs):
        plt.subplot(1, len(imgs), i + 1)
        plt.imshow(img, cmap='gray')
        plt.title('Sample Image' if i == 0 else 'Reference Image')
        plt.axis('off')
    plt.show()

def uploadTrafficImage():
    global filename
    filename = filedialog.askopenfilename(initialdir="images")
    pathlabel.config(text=filename)

    # Call functions after image selection
    applyCanny()
    pixelcount()
    timeAllocation()

def applyCanny():
    imgs = []
    img = mpimg.imread(filename)
    img = rgb2gray(img)
    imgs.append(img)
    edge = CannyEdgeDetector(imgs, sigma=1.4, kernel_size=5,
                             lowthreshold=0.09, highthreshold=0.20, weak_pixel=100)
    imgs = edge.detect()
    for i, img in enumerate(imgs):
        if img.shape[0] == 3:
            img = img.transpose(1, 2, 0)
    cv2.imwrite("gray/test.png", img)
    temp = []
    img1 = mpimg.imread('gray/test.png')
    img2 = mpimg.imread('gray/refrence.png')
    temp.append(img1)
    temp.append(img2)
    visualize(temp)

def pixelcount():
    global refrence_pixels, sample_pixels
    img = cv2.imread('gray/test.png', cv2.IMREAD_GRAYSCALE)
    sample_pixels = np.sum(img == 255)

    img = cv2.imread('gray/refrence.png', cv2.IMREAD_GRAYSCALE)
    refrence_pixels = np.sum(img == 255)
    messagebox.showinfo("Pixel Counts", f"Total Sample White Pixels Count : {sample_pixels}\nTotal Reference White Pixels Count : {refrence_pixels}")

def timeAllocation():
    avg = (sample_pixels / refrence_pixels) * 100
    if avg >= 100:
        message = "Traffic is very high allocation green signal time : 60 secs"
    elif 80 <= avg < 100:
        message = "Traffic is high allocation green signal time : 50 secs"
    elif 60 < avg <= 80:
        message = "Traffic is moderate green signal time : 40 secs"
    elif 40 < avg <= 60:
        message = "Traffic is low allocation green signal time : 30 secs"
    else:
        message = "Traffic is very low allocation green signal time : 10 secs"

    messagebox.showinfo("Green Signal Allocation Time", message)

font = ('Arial', 14)
title = Label(main, text='Density Based Smart Traffic Control System', font=(font[0], 20, 'bold'), bg='lightblue')
title.pack(pady=10)

upload_button = Button(main, text="Upload Traffic Image", command=uploadTrafficImage, font=font, bg='orange', fg='white')
upload_button.pack()

pathlabel = Label(main, text="Selected Image Path: ", font=font, bg='lightgreen')
pathlabel.pack(pady=5)

main.mainloop()
