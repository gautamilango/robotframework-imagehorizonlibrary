# -*- coding: utf-8 -*-

from tkinter import Image
from src.ImageHorizonLibrary import ImageHorizonLibrary

#ih = ImageHorizonLibrary(reference_folder='..\\..\\images', strategy='skimage')
ih = ImageHorizonLibrary(reference_folder='..\\..\\images', strategy='pyautogui')
# ih.wait_for(reference_image='foo')
foo = ih.click_image("win")

pass