import pyautogui as ag
from tkinter import filedialog as fd
import matplotlib.pyplot as plt


class UILocatorModel():
    def capture_desktop(self):
        return ag.screenshot()

    def plot_result(self, needle_img, haystack_img, needle_img_edges, haystack_img_edges, peakmap, title, coord):
        fig, axs = plt.subplots(2, 3)
        sp_haystack_img = axs[0, 0]
        sp_needle_img = axs[0, 1]
        sp_invisible = axs[0, 2]
        sp_haystack_img_edges = axs[1, 0]
        sp_needle_img_edges = axs[1, 1]
        sp_peakmap = axs[1, 2]
        
        # ROW 1 ================================
        sp_needle_img.imshow(needle_img, cmap=plt.cm.gray)
        sp_needle_img.set_title('Needle image')
        sp_haystack_img.imshow(haystack_img, cmap=plt.cm.gray)

        sp_haystack_img.set_title('Haystack image')
        sp_haystack_img.sharex(sp_haystack_img_edges)
        sp_haystack_img.sharey(sp_haystack_img_edges)

        sp_invisible.set_visible(False)

        # ROW 2 ================================
        sp_needle_img_edges.imshow(needle_img_edges, cmap=plt.cm.gray)    
        sp_needle_img_edges.set_title('Needle image edges')

        sp_haystack_img_edges.imshow(haystack_img_edges, cmap=plt.cm.gray)
        sp_haystack_img_edges.set_title('Haystack image edges')

        sp_peakmap.imshow(peakmap)
        sp_peakmap.set_title('Peakmap')
        sp_peakmap.sharex(sp_haystack_img_edges)
        sp_peakmap.sharey(sp_haystack_img_edges)
        
        for loc in coord:
            # highlight matched region
            #needle_img_height, needle_img_width = needle_img_edges.shape
            # TODO: 
            #rect = plt.Rectangle((x_peak-int(needle_img_width/2), y_peak-int(needle_img_height/2)), needle_img_width, needle_img_height, edgecolor='r', facecolor='none')
            rect = plt.Rectangle((loc[0], loc[1]), loc[2], loc[3], edgecolor='r', facecolor='none')
            sp_haystack_img_edges.add_patch(rect)

        
        sp_peakmap.autoscale(False)    
        fig.suptitle(title, fontsize=14, fontweight='bold')
        
        plt.show()