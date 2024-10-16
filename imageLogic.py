from jes4py import *
import tkinter as tk
from tkinter import filedialog, messagebox

image = None
original_image = None


def load_picture():
    file = pickAFile()

    global image
    image = makePicture(file)

    global original_image
    original_image = duplicatePicture(image)


def change_color(r, g, b):
    if image is None:
        print("No image loaded! Please load an image first.")
        return

    for p in getPixels(image):
        rValue = getRed(p)
        setRed(p, rValue * r)

        gValue = getGreen(p)
        setGreen(p, gValue * g)

        bValue = getBlue(p)
        setBlue(p, bValue * b)

    explore(image)


def rotate_image(degrees):
    global image
    # Calculate the number of 90-degree rotations needed
    rotations = (degrees // 90) % 4  # Ensure it stays within 0 to 3 rotations

    for _ in range(rotations):
        # Create a new picture (canvas) with swapped dimensions for 90-degree rotation
        width = getWidth(image)
        height = getHeight(image)
        rotated_canvas = makeEmptyPicture(height, width)

        # Loop through each pixel in the original image
        for x in range(0, width):
            for y in range(0, height):
                # Get the color of the current pixel
                color = getColor(getPixel(image, x, y))

                # 90-degree rotation (clockwise)
                setColor(getPixel(rotated_canvas, y, width - x - 1), color)

        # Update the image to the newly rotated one for further rotations
        image = rotated_canvas

    # Show the final rotated image
    explore(image)
    return image


def scale(scale_factor):
    global image  # Save the result in the global image variable

    # Set up the source and target pictures
    width = getWidth(image)
    height = getHeight(image)

    # If the scale factor is less than 1, shrink the canvas
    if scale_factor < 1:
        # Create the target (shrunk) canvas with scaled-down dimensions
        canvas = makeEmptyPicture(int(width * scale_factor), int(height * scale_factor))

        # Now, do the actual copying
        for targetX in range(0, getWidth(canvas)):
            for targetY in range(0, getHeight(canvas)):
                # Calculate corresponding source pixels in the original image
                sourceX = int(targetX / scale_factor)
                sourceY = int(targetY / scale_factor)

                # Get the color from the corresponding source pixel
                color = getColor(getPixel(image, sourceX, sourceY))

                # Set the color to the shrunk canvas
                setColor(getPixel(canvas, targetX, targetY), color)

    else:
        # If the scale factor is greater than 1, enlarge the canvas
        canvas = makeEmptyPicture(int(width * scale_factor), int(height * scale_factor))

        for targetX in range(0, getWidth(canvas)):
            for targetY in range(0, getHeight(canvas)):
                # Calculate corresponding source pixels in the original image
                sourceX = int(targetX / scale_factor)
                sourceY = int(targetY / scale_factor)

                # Get the color from the corresponding source pixel
                color = getColor(getPixel(image, sourceX, sourceY))

                # Set the color to the enlarged canvas
                setColor(getPixel(canvas, targetX, targetY), color)

    # Update the global image with the new scaled version (shrunk or enlarged)
    image = canvas

    # Show the scaled image
    show(image)
    return image


def posterize(levels):
    # Calculate the interval size for each level
    interval_size = 256 // levels  # The size of each "bin"

    # Loop through the pixels
    for p in getPixels(image):
        # Get the RGB values
        red = getRed(p)
        green = getGreen(p)
        blue = getBlue(p)

        # Posterize the red value
        if levels == 2:
            new_red = 0 if red < 128 else 255  # Force values to either 0 or 255
        else:
            new_red = (red // interval_size) * interval_size
        setRed(p, new_red)

        # Posterize the green value
        if levels == 2:
            new_green = 0 if green < 128 else 255  # Force values to either 0 or 255
        else:
            new_green = (green // interval_size) * interval_size
        setGreen(p, new_green)

        # Posterize the blue value
        if levels == 2:
            new_blue = 0 if blue < 128 else 255  # Force values to either 0 or 255
        else:
            new_blue = (blue // interval_size) * interval_size
        setBlue(p, new_blue)

    # Return the modified picture
    explore(image)


def save_picture():
    # Initialize Tkinter root (but hide the main window)
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Check if the image exists
    if image is None:
        messagebox.showerror("Error", "No image to save.")
        return

    # Open a save dialog and let the user choose the file name and format
    file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])

    # If a path is selected, save the image using JES writePictureTo
    if file_path:
        try:
            writePictureTo(image, file_path)  # Use JES function to save the image
            print(f"Image successfully saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {e}")


def reset_image():
    global image
    global original_image

    image = duplicatePicture(original_image)

    explore(image)