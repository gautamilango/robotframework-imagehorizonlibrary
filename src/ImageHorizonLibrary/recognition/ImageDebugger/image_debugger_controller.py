from .image_debugger_model import UILocatorModel
from .image_debugger_view import UILocatorView
from .template_matching_strategies import Pyautogui, Skimage
from .image_manipulation import ImageContainer, ImageFormat
from pathlib import Path
import os, glob
import pyperclip


class UILocatorController:

    def __init__(self, image_horizon_instance):
        self.image_container = ImageContainer()
        self.model = UILocatorModel()
        self.image_horizon_instance = image_horizon_instance
        self.view = UILocatorView(self, self.image_container, self.image_horizon_instance)
        
    def main(self):
        self.init_view()
        self.view.main()

    def init_view(self):
        self.view.ref_dir_path.set(self.image_horizon_instance.reference_folder)
        self.view.conf_lvl_ag.set('0.99')
        self.view.edge_sigma_skimage.set("2.0")
        self.view.edge_low_skimage.set("0.1")
        self.view.edge_high_skimage.set("0.3")
        self.view.conf_lvl_skimage.set("0.99")
        self.view.executed_strategy.set("None")
        self.view.matches_found.set("0")
        self.view.btn_edge_detection_debugger["state"] = "disabled"
        self.view.btn_run_pyautogui["state"] = "disabled"
        self.view.btn_run_skimage["state"] = "disabled"
        self.view.btn_copy_strategy_snippet["state"] = "disabled"
        self.view.statusOrHints.set("Ready")

    def create_list_of_images(self, reference_folder):
        os.chdir(reference_folder)
        list_needle_images_names = []
        for needle_img_name in glob.glob("*.png"):
            list_needle_images_names.append(needle_img_name)
        return list_needle_images_names

    def copy_to_clipboard(self):
        pyperclip.copy(self.strategy_snippet)

    def on_select(self, event):
        ref_image = Path(self.view.combobox_needle_img_name.get())
        self.image_container.save_to_img_container(img=ref_image.__str__())
        self.needle_img = self.image_container.get_needle_image(ImageFormat.IMAGETK)
        self.view.canvas_ref_img.itemconfig(
            self.view.ref_img,
            image=self.needle_img,
        )

        self.view.btn_run_pyautogui["state"] = "normal"
        self.view.btn_run_skimage["state"] = "normal"

    def _take_screenshot(self):
        # Minimize the GUI Debugger window before taking the screenshot
        self.view.wm_state('iconic')
        screenshot = self.model.capture_desktop()
        self.view.wm_state('normal')
        return screenshot
    
    def on_click_run_pyautogui(self):
        self.image_horizon_instance.set_strategy('pyautogui')
        self.image_horizon_instance.confidence = float(self.view.spinbox_conf_lvl_ag.get())
        self.image_container.save_to_img_container(self._take_screenshot(), is_haystack_img=True)

        matcher = Pyautogui(self.image_container, self.image_horizon_instance)
        self.coord = matcher.find_num_of_matches()
        matcher.highlight_matches()

        self.haystack_image = self.image_container.get_haystack_image(format=ImageFormat.IMAGETK)
        self.view.canvas_desktop_img.itemconfig(self.view.desktop_img, image=self.haystack_image)

        self.view.executed_strategy.set('pyAutoGui')
        num_of_matches_found = len(self.coord)
        self.view.matches_found.set(num_of_matches_found)
        font_color = self.model.change_color_of_label(num_of_matches_found)
        self.view.label_matches_found.config(fg=font_color)

        self.strategy_snippet = f"Set Strategy  pyautogui  confidence={self.image_horizon_instance.confidence}"
        self.view.set_strategy_snippet.set(self.strategy_snippet)
        self.view.btn_copy_strategy_snippet["state"] = "normal"


    def on_click_run_skimage(self):
        self.image_horizon_instance.set_strategy('skimage')
        self.image_horizon_instance.confidence = float(self.view.spinbox_conf_lvl_skimage.get())
        self.image_horizon_instance.edge_sigma = float(self.view.spinbox_edge_sigma_skimage.get())
        self.image_horizon_instance.edge_low_threshold = float(self.view.spinbox_edge_low_skimage.get())
        self.image_horizon_instance.edge_high_threshold = float(self.view.spinbox_edge_high_skimage.get())
        self.image_container._haystack_image_orig_size = self._take_screenshot()

        matcher = Skimage(self.image_container, self.image_horizon_instance)
        self.coord = matcher.find_num_of_matches()
        matcher.highlight_matches()

        self.haystack_image = self.image_container.get_haystack_image(format=ImageFormat.IMAGETK)
        self.view.canvas_desktop_img.itemconfig(self.view.desktop_img, image=self.haystack_image)

        self.view.executed_strategy.set('Skimage')
        num_of_matches_found = len(self.coord)
        self.view.matches_found.set(num_of_matches_found)
        font_color = self.model.change_color_of_label(num_of_matches_found)
        self.view.label_matches_found.config(fg=font_color)
        self.view.btn_edge_detection_debugger["state"] = "normal"

        self.strategy_snippet = f"Set Strategy  skimage  edge_sigma={self.image_horizon_instance.edge_sigma}  edge_low_threshold={self.image_horizon_instance.edge_low_threshold}  edge_high_threshold={self.image_horizon_instance.edge_high_threshold}  confidence={self.image_horizon_instance.confidence}"
        self.view.set_strategy_snippet.set(self.strategy_snippet)
        self.view.btn_copy_strategy_snippet["state"] = "normal"


    def on_click_plot_results_skimage(self):
        title = f"{self.view.matches_found.get()} matches (confidence: {self.image_horizon_instance.confidence})"
        self.model.plot_result(
            self.image_container.get_needle_image(ImageFormat.NUMPYARRAY),
            self.image_container.get_haystack_image_orig_size(ImageFormat.NUMPYARRAY),
            self.image_horizon_instance.needle_edge,
            self.image_horizon_instance.haystack_edge,
            self.image_horizon_instance.peakmap,
            title,
            self.coord
            )
