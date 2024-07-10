from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
import numpy as np
from tkinter.filedialog import askopenfilename
import numpy as np
from CannyEdgeDetector import *
import skimage
import matplotlib.image as mpimg
import os
import scipy.misc as sm
import cv2
import matplotlib.pyplot as plt

main = tkinter.Tk()
main.title("Density Based Smart Traffic Control System")
main.geometry("1300x1200")

global filename
global refrence_pixels
global sample_pixels


def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray


def visualize(imgs, format=None, gray=False):
    j = 0
    plt.figure(figsize=(20, 40))
    for i, img in enumerate(imgs):
        if img.shape[0] == 3:
            img = img.transpose(1, 2, 0)
        plt_idx = i+1
        plt.subplot(2, 2, plt_idx)
        if j == 0:
            plt.title('Sample Image')
            plt.imshow(img, format)
            j = j + 1
        elif j > 0:
            plt.title('Reference Image')
            plt.imshow(img, format)
    plt.show()


def uploadTrafficImage():
    option = messagebox.askquestion("Choose Option", "Do you want to upload an image file?")
    if option == 'yes':
        filename = filedialog.askopenfilename(initialdir="images")
        pathlabel.config(text=filename)
        # Call functions after image selection
        applyCanny(filename)
        pixelcount()
        timeAllocation()
    else:
        captureFromCamera()


def captureFromCamera():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if ret:
        cv2.imwrite("captured_image.png", frame)
        filename = "captured_image.png"
        pathlabel.config(text=filename)
        # Call functions after image selection
        applyCanny(filename)
        pixelcount()
        timeAllocation()
    else:
        messagebox.showerror("Error", "Failed to capture image from camera.")


def applyCanny(filename):
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
    global refrence_pixels
    global sample_pixels
    img = cv2.imread('gray/test.png', cv2.IMREAD_GRAYSCALE)
    sample_pixels = np.sum(img == 255)

    img = cv2.imread('gray/refrence.png', cv2.IMREAD_GRAYSCALE)
    refrence_pixels = np.sum(img == 255)
    messagebox.showinfo("Pixel Counts", "Total Sample White Pixels Count : "+str(
        sample_pixels)+"\nTotal Refrence White Pixels Count : "+str(refrence_pixels))


def timeAllocation():
    avg = (sample_pixels/refrence_pixels) * 100
    if avg >= 100:
        messagebox.showinfo("Green Signal Allocation Time",
                            "Traffic is very high allocation green signal time : 60 secs")
    if avg > 80 and avg < 100:
        messagebox.showinfo("Green Signal Allocation Time",
                            "Traffic is high allocation green signal time : 50 secs")
    if avg > 60 and avg <= 80:
        messagebox.showinfo("Green Signal Allocation Time",
                            "Traffic is moderate green signal time : 40 secs")
    if avg > 40 and avg <= 60:
        messagebox.showinfo("Green Signal Allocation Time",
                            "Traffic is low allocation green signal time : 30 secs")
    if avg <= 40:
        messagebox.showinfo("Green Signal Allocation Time",
                            "Traffic is very low allocation green signal time : 10 secs")


def exit():
    main.destroy()


font = ('Arial', 14)
title = Label(main, text='Density Based Smart Traffic Control System', font=(font[0], 20, 'bold'), bg='lightblue')
title.pack(pady=10)

upload_button = Button(main, text="Upload Traffic Image", command=uploadTrafficImage, font=font, bg='orange', fg='white')
upload_button.pack()

pathlabel = Label(main, text="Selected Image Path: ", font=font, bg='lightgreen')
pathlabel.pack(pady=5)

main.mainloop()
