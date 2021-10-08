import numpy as np
import matplotlib.pyplot as plt

from skimage import data
from skimage.feature import match_template
from skimage.feature import peak_local_max
import skimage.viewer
from skimage.color import rgb2gray
import pyautogui as ag
import sys

image = data.coins()
coin = image[170:220, 75:130]


image = rgb2gray(np.array(ag.screenshot()))
#image = skimage.io.imread('..\\..\\images\\screen.png', as_gray=True)

coin = skimage.io.imread('..\\..\\images\\win.png', as_gray=True)
#coin = skimage.io.imread('..\\..\\images\\text.png', as_gray=True)
#coin = skimage.io.imread('..\\..\\images\\win_changed.png', as_gray=True)

#skimage.viewer.ImageViewer(image).show()
# ---
# result = match_template(image, coin,pad_input=True) #added the pad_input bool
# peak_min_distance = min(coin.shape)
# peak_min_distance = 1

# peaks = peak_local_max(result,min_distance=peak_min_distance,threshold_abs=1)
# # produce a plot equivalent to the one in the docs
# plt.imshow(result)
# # highlight matched regions (plural)
# plt.plot(peaks[:,1], peaks[:,0], 'o', markeredgecolor='r', markerfacecolor='none', markersize=10)
# plt.show()
# ---


def compare():
    confidence = 0.9999999999999
    #confidence = 0.9

    result = match_template(image, coin, pad_input=True)
    ij = np.unravel_index(np.argmax(result), result.shape)
    x, y = ij[::-1]
    
    fig = plt.figure(figsize=(8, 3))
    ax1 = plt.subplot(1, 3, 1)
    ax2 = plt.subplot(1, 3, 2)
    ax3 = plt.subplot(1, 3, 3, sharex=ax2, sharey=ax2)

    ax1.imshow(coin, cmap=plt.cm.gray)
    #ax1.set_axis_off()
    ax1.set_title('what')

    ax2.imshow(image, cmap=plt.cm.gray)
    #ax2.set_axis_off()
    ax2.set_title('where')
    # highlight matched region
    hcoin, wcoin = coin.shape
    rect = plt.Rectangle((x-int(wcoin/2), y-int(hcoin/2)), wcoin, hcoin, edgecolor='r', facecolor='none')
    ax2.add_patch(rect)

    ax3.imshow(result)
    #ax3.set_axis_off()
    ax3.set_title('peak map')
    # highlight matched region
    ax3.autoscale(False)
    ax3.plot(x, y, 'o', markeredgecolor='r', markerfacecolor='none', markersize=10)

    peak = result[y][x]
    matched = peak > confidence
    suptitle = f"Match = {str(matched)} (peak at {peak} > {confidence})"
    fig.suptitle(suptitle, fontsize=14, fontweight='bold')

    plt.show()
    pass

compare()
#cProfile.run('compare()')

# confidence:            0.9999999999999
# win auf screen:        0.9999999999999992
# win auf screenshot:    0.9999999999999974
# win_ch auf screen:     0.9999999419440094
# win_ch auf screenshot: 0.9999999419440035

