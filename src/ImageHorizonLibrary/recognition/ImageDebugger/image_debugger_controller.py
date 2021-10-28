from .image_debugger_model import UILocatorModel
from .image_debugger_view import UILocatorView
from .template_matching_strategies import Pyautogui, Skimage
from .image_manipulation import ImageContainer, ImageFormat
import os


class UILocatorController:

    def __init__(self, image_horizon_instance):
        self.image_container = ImageContainer()
        self.model = UILocatorModel()
        self.image_horizon_instance = image_horizon_instance
        self.view = UILocatorView(self, self.image_container, self.image_horizon_instance)

    def main(self):
        self.view.main()

    def on_select(self, event):
        ref_images_path = self.image_horizon_instance.reference_folder
        path_to_ref_image = os.path.join(ref_images_path, self.view.combobox_needle_img_name.get())
        self.image_container.save_to_img_container(img=path_to_ref_image)
        self.needle_img = self.image_container.get_needle_image(ImageFormat.IMAGETK)
        self.view.canvas_ref_img.itemconfig(
            self.view.ref_img,
            image=self.needle_img,
        )

    def _take_screenshot(self):
        # Minimize the GUI Debugger window before taking the screenshot
        self.view.wm_state('iconic')
        screenshot = self.model.capture_desktop()
        self.view.wm_state('normal')
        return screenshot
    
    def on_click_run_pyautogui(self):
        self.view.executed_strategy.set('pyAutoGui')
        self.image_horizon_instance.set_strategy('pyautogui')
        self.image_horizon_instance.confidence = self.view.spinbox_conf_lvl_ag.get()
        self.image_container.save_to_img_container(self._take_screenshot(), is_haystack_img=True)

        matcher = Pyautogui(self.image_container, self.image_horizon_instance)

        self.coord = matcher.find_num_of_matches()
        num_of_matches_found = len(self.coord)
        self.view.matches_found.set(num_of_matches_found)
        if(num_of_matches_found == 1):
            self.view.label_matches_found.config(fg='green')
        else:
            self.view.label_matches_found.config(fg='red')

        matcher.highlight_matches()
        self.haystack_image = self.image_container.get_haystack_image(format=ImageFormat.IMAGETK)
        self.view.canvas_desktop_img.itemconfig(self.view.desktop_img, image=self.haystack_image)

    def on_click_run_skimage(self):
        self.view.executed_strategy.set('Skimage')
        self.image_horizon_instance.set_strategy('skimage')
        self.image_horizon_instance.confidence = float(self.view.spinbox_conf_lvl_skimage.get())
        self.image_horizon_instance.edge_sigma = float(self.view.spinbox_edge_sigma_skimage.get())
        self.image_horizon_instance.edge_low_threshold = float(self.view.spinbox_edge_low_skimage.get())
        self.image_horizon_instance.edge_high_threshold = float(self.view.spinbox_edge_high_skimage.get())
        self.image_container._haystack_image_orig_size = self._take_screenshot()

        matcher = Skimage(self.image_container, self.image_horizon_instance)

        self.coord = matcher.find_num_of_matches()
        num_of_matches_found = len(self.coord)
        self.view.matches_found.set(num_of_matches_found)
        if(num_of_matches_found == 1):
            self.view.label_matches_found.config(fg='green')
        else:
            self.view.label_matches_found.config(fg='red')

        matcher.highlight_matches()
        self.haystack_image = self.image_container.get_haystack_image(format=ImageFormat.IMAGETK)
        self.view.canvas_desktop_img.itemconfig(self.view.desktop_img, image=self.haystack_image)


    def on_click_plot_results_skimage(self):
        needle_img = self.image_container.get_needle_image(ImageFormat.NUMPYARRAY)
        haystack_img = self.image_container.get_haystack_image(ImageFormat.NUMPYARRAY)
        needle_img_edges = self.image_horizon_instance.needle_edge
        haystack_img_edges = self.image_horizon_instance.haystack_edge
        peakmap = self.image_horizon_instance.peakmap
        title = f"{self.view.matches_found.get()} matches (confidence: {self.image_horizon_instance.confidence})"
        coord = self.coord
        self.model.plot_result(needle_img, haystack_img, needle_img_edges, haystack_img_edges, peakmap, title, coord)
