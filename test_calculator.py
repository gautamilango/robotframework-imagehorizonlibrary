# -*- coding: utf-8 -*-
# Run this test while the Windows 10 calculator is already open


from src.ImageHorizonLibrary import ImageHorizonLibrary

#ih = ImageHorizonLibrary(reference_folder='..\\..\\images', strategy='skimage')
ih = ImageHorizonLibrary(reference_folder='..\\..\\images', strategy='pyautogui')
# ih.does_exist("win")
# foo = ih.click_image("win")
# ih.set_strategy('skimage', edge_sigma=2, edge_low_threshold=0.1, edge_high_threshold=0.3)
# foo = ih.click_image("win")
# ih.set_strategy('skimage', edge_sigma=4, edge_low_threshold=0.2, edge_high_threshold=0.4)
# ih.set_strategy('pyautogui')
# ih.set_strategy('pyautogui')


ih.wait_for('3')
ih.click_image('3')
ih.click_image('plus')
ih.click_image('7')
ih.click_image('equal')
ih.wait_for('10')
pass