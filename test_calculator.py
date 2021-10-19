# -*- coding: utf-8 -*-
# Run this test while the Windows 10 calculator is already open

from ImageHorizonLibrary import ImageHorizonLibrary
import numpy as np
import pyautogui as ag

# from src.ImageHorizonLibrary import ImageHorizonLibrary

#ih = ImageHorizonLibrary(reference_folder='..\\..\\images', strategy='pyautogui')
#ih = ImageHorizonLibrary(reference_folder='..\\..\\images', strategy='skimage', edge_sigma=1.0)
# ih.does_exist("win")
ih = ImageHorizonLibrary(reference_folder='..\\..\\images', strategy='skimage')

haystack_image = np.array(ag.screenshot())
foo = ih._locate_all("foo", haystack_image)
# foo = ih._locate_all("ok")
#foo = ih.click_image("win")
# ih.set_strategy('skimage', edge_sigma=2, edge_low_threshold=0.1, edge_high_threshold=0.3)
# foo = ih.click_image("win")
# ih.set_strategy('skimage', edge_sigma=4, edge_low_threshold=0.2, edge_high_threshold=0.4)
# ih.set_strategy('pyautogui')
# ih.set_strategy('pyautogui')


# ih.set_strategy('pyautogui')

#ih.wait_for('ih_click_image')


ih.wait_for('3')
ih.click_image('3')
ih.click_image('plus')
ih.click_image('7')
ih.click_image('equal')
ih.wait_for('10')
pass

# Fooo

# Fooo

# Fooo

# Fooo

# Fooo

# Fooo

# Fooo

