# -*- coding: utf-8 -*-

# from tkinter import Image
from src.ImageHorizonLibrary import ImageHorizonLibrary

#ih = ImageHorizonLibrary(reference_folder='..\\..\\images', strategy='skimage', edge_sigma=2, edge_low_threshold=1, edge_high_threshold=2)
ih = ImageHorizonLibrary(reference_folder='..\\..\\images', strategy='skimage')
foo = ih.click_image("win")
#ih = ImageHorizonLibrary(reference_folder='..\\..\\images', strategy='pyautogui')
# ih.wait_for(reference_image='foo')
# ih.set
# pass
import sys
sys.exit(1)


#----------


import pyautogui as ag

import skimage
import skimage.feature
import skimage.viewer
from skimage.feature import match_template
from skimage.metrics import structural_similarity as ssim
from skimage.color import rgb2gray
import skimage.io
import numpy as np
from PIL import Image, ImageFilter

# Screenhot vom Desktop (Pillow _ Image)
# Konvertieren in skimage-Matrix
screen = rgb2gray(np.array(ag.screenshot()))
skimage.viewer.ImageViewer(screen).show()
ref_image = skimage.io.imread('..\\..\\images\\win.png', as_gray=True)
result = match_template(screen, ref_image)
skimage.viewer.ImageViewer(result).show()
print("foo")
pass



# Lade Referenzbild (skimage) 

# Edgedetection auf beide Bilder


def compare_images_using_edge_detection(reference_image_path, comparee_path):
    # https://datacarpentry.org/image-processing/08-edge-detection/index.html
    sigma = 2.0
    low_threshold = 0.1
    high_threshold = 0.3
    # Read image 1
    refImage = skimage.io.imread(fname=reference_image_path, as_gray=True)
    # refEdges = skimage.feature.canny(
    #     image=refImage,
    #     sigma=sigma,
    #     low_threshold=low_threshold,
    #     high_threshold=high_threshold,
    # )
    # Read image 2
    compImage = skimage.io.imread(fname=comparee_path, as_gray=True)
    # compEdges = skimage.feature.canny(
    #     image=compImage,
    #     sigma=sigma,
    #     low_threshold=low_threshold,
    #     high_threshold=high_threshold,
    # )
    # For debugging: show images
    #skimage.viewer.ImageViewer(refImage).show()
    #skimage.viewer.ImageViewer(compImage).show()
    
    # https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/
    # Similarity of edge images
    #similarity = ssim(refEdges, compEdges)
    # Similarity of original images
    similarity = ssim(refImage, compImage)
    return similarity