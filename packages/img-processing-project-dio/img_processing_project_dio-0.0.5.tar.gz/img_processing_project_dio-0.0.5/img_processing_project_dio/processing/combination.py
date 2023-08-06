from matplotlib import image
import numpy as np
from skimage.color import rgb2gray
from skimage.exposure import match_histograms
from skimage.metrics import structural_similarity

def find_difference(image_1, image_2):
    assert image_1.shape == image_2.shape, "Specify 2 imagens with same shape"
    gray_image_1 = rgb2gray(image_1)
    gray_image_2 = rgb2gray(image_2)
    (score, difference_image) = structural_similarity(gray_image_1, gray_image_2, full = True)
    print("Similarity of the images", score)
    normalized_difference_image = (difference_image - np.min(difference_image))/(np.max(difference_image) - np.min(difference_image))
    return normalized_difference_image

def transfer_histogram(image_1, image_2):
    matched_image = match_histograms(image_1, image_2, channel_axis=True)
    return matched_image