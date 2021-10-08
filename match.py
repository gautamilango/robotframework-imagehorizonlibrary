import numpy as np
import matplotlib.pyplot as plt

from skimage import data
from skimage.feature import match_template
from skimage.feature import peak_local_max
import skimage.viewer
from skimage.color import rgb2gray
import pyautogui as ag
import sys

screen = data.coins()
coin = screen[170:220, 75:130]



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


def detect_edges(img, sigma, low, high):
    edge_img = skimage.feature.canny(
        image=img,
        sigma=sigma,
        low_threshold=low,
        high_threshold=high,
    )
    return edge_img


def plot_result(what, where, peakmap, title, x_peak, y_peak):    
    fig = plt.figure(figsize=(8, 3))
    ax1 = plt.subplot(1, 3, 1)
    ax2 = plt.subplot(1, 3, 2)
    ax3 = plt.subplot(1, 3, 3, sharex=ax2, sharey=ax2)

    ax1.imshow(what, cmap=plt.cm.gray)
    #ax1.set_axis_off()
    ax1.set_title('what')

    ax2.imshow(where, cmap=plt.cm.gray)
    #ax2.set_axis_off()
    ax2.set_title('where')
    # highlight matched region
    hwhat, wwhat = what.shape
    rect = plt.Rectangle((x_peak-int(wwhat/2), y_peak-int(hwhat/2)), wwhat, hwhat, edgecolor='r', facecolor='none')
    ax2.add_patch(rect)

    ax3.imshow(peakmap)
    #ax3.set_axis_off()
    ax3.set_title('peakmap')
    # highlight matched region
    ax3.autoscale(False)
    ax3.plot(x_peak, y_peak, 'o', markeredgecolor='r', markerfacecolor='none', markersize=10)


    fig.suptitle(title, fontsize=14, fontweight='bold')
    plt.show()


def compare(what_name, sigma=2.0, low=0.1, high=0.3, confidence=0.9999999999999):
    what = skimage.io.imread('..\\..\\images\\' + what_name, as_gray=True)
    where = rgb2gray(np.array(ag.screenshot()))
    what_edge = detect_edges(what, sigma, low, high)
    what_where = detect_edges(where, sigma, low, high)
    peakmap = match_template(what_where, what_edge, pad_input=True)
    ij = np.unravel_index(np.argmax(peakmap), peakmap.shape)
    x, y = ij[::-1]

    peak = peakmap[y][x]
    matched = peak > confidence
    title = f"Match = {str(matched)} (peak at {peak} > {confidence})"
#    plot_result(what, where, peakmap, title, x,y)
    plot_result(what_edge, what_where, peakmap, title, x,y)
    

#image = skimage.io.imread('..\\..\\images\\screen.png', as_gray=True)


compare('3.png')
#cProfile.run('compare()')

# confidence:            0.9999999999999
# win auf screen:        0.9999999999999992
# win auf screenshot:    0.9999999999999974
# win_ch auf screen:     0.9999999419440094
# win_ch auf screenshot: 0.9999999419440035

