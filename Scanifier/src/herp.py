from PIL import Image
import numpy as np

def binarize_array(numpy_array, threshold=120):
    """Binarize a numpy array."""
    for i in range(len(numpy_array)):
        for j in range(len(numpy_array[0])):
            if numpy_array[i][j] > threshold:
                numpy_array[i][j] = 255
            else:
                numpy_array[i][j] = 0
    return numpy_array

def crop_image(image):
    image = image.convert('L')
    image_array=np.array(image)
    bw_array=binarize_array(image_array)
    bw_image=Image.fromarray(bw_array)
    bw_image.show()

    height,width= image_array.shape
    middle_x=width/2
    middle_y=height/2
    # image.show()

written_image = Image.open("../data/handwriting.jpg")
crop_image(written_image)