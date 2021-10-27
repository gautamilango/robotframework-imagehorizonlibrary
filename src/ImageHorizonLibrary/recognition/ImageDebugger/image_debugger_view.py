from os import path
import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
from .image_manipulation import ImageFormat
import glob, os


class UILocatorView(Tk):
    def __init__(self, controller, image_container, image_horizon_instance):
        super().__init__()
        self.title("GUI Debugger")
        self.resizable(False, False)
        self.controller = controller
        self.image_container = image_container
        self.image_horizon_instance = image_horizon_instance
        self.def_save_loc = tk.StringVar()
        self.ref_img_loc = tk.StringVar()
        self.needle_img = ImageTk.PhotoImage(Image.new('RGB', (30, 30), color='white'))
        self.haystack_img = ImageTk.PhotoImage(Image.new('RGB', (384, 216), color='white'))
        self._create_view()

    def main(self):
        self.mainloop()

    def _create_view(self):
        self._frame_main()
        self._frame_load_reference_image()
        self._frame_computation_params()
        self._frame_results()
        self._frame_image_viewer()

    def _frame_main(self):
        # *************** Frame Main *************** #
        self.frame_main = Frame(self)
        self.frame_main.pack(side=TOP, padx=10, pady=10)

    def _frame_load_reference_image(self):
        # ************ Frame Select image ************ #
        frame_import_ref_image = LabelFrame(self.frame_main, text="Select reference image (.png)", padx=10, pady=10)
        frame_import_ref_image.pack(side=TOP, padx=10, pady=10, fill=X)

        os.chdir("C:\\Users\\exgil01\\Documents\\RobotFramework-DEV\\robot-e2e\\images")

        # list_images = self.image_horizon_instance.reference_folder
        list_needle_images_names = []
        for needle_img_name in glob.glob("*.png"):
            list_needle_images_names.append(needle_img_name)
        self.combobox_needle_img_name = ttk.Combobox(frame_import_ref_image, value=list_needle_images_names, width=10, state="readonly")
        self.combobox_needle_img_name.pack(fill=X)
        self.combobox_needle_img_name.bind("<<ComboboxSelected>>", self.controller.on_select)
    
    def _frame_computation_params(self):
        # ************ Frame Computation ************ #
        frame_computation = LabelFrame(self.frame_main, text="Computation", padx=10, pady=10)
        frame_computation.pack(side=TOP, padx=10, pady=10, fill=X)

        frame_computation.columnconfigure(0, weight=1)
        frame_computation.columnconfigure(1, weight=1)
        
        # ************ Frame Strategy pyAutogui ************* #
        frame_strat_pyautogui = LabelFrame(frame_computation, text="Strategy pyAutoGui", padx=5, pady=5)
        frame_strat_pyautogui.grid(row=0, column=0, padx=10, pady=10, sticky="WNS")

        frame_strat_pyautogui.columnconfigure(0, weight=3)
        frame_strat_pyautogui.columnconfigure(1, weight=1)

        Label(frame_strat_pyautogui, text="Confidence level").grid(row=0, column=0, sticky=W)
        conf_lvl_ag = StringVar(frame_strat_pyautogui)
        conf_lvl_ag.set("0.99")
        self.spinbox_conf_lvl_ag = Spinbox(frame_strat_pyautogui, from_=0, to=1, increment=0.01, width=4, textvariable=conf_lvl_ag)
        self.spinbox_conf_lvl_ag.grid(padx=(30, 0), row=0, column=1, sticky=E)

        Button(frame_computation, text='Run Strategy pyAutoGui', command=self.controller.on_click_run_pyautogui).grid(row=1, column=0, padx=10, sticky=W)

        # ************ Frame Strategy skimage ************ #
        frame_strat_skimage = LabelFrame(frame_computation, text="Strategy skimage", padx=5, pady=5)
        frame_strat_skimage.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        frame_strat_skimage.columnconfigure(0, weight=3)
        frame_strat_skimage.columnconfigure(1, weight=1)
        
        Label(frame_strat_skimage, text="Edge sigma").grid(row=0, column=0, sticky=W)
        edge_sigma_skimage = StringVar(frame_strat_skimage)
        edge_sigma_skimage.set("2.0")
        self.spinbox_edge_sigma_skimage = Spinbox(frame_strat_skimage, from_=0, to=5, increment=0.01, width=4, textvariable=edge_sigma_skimage)
        self.spinbox_edge_sigma_skimage.grid(padx=(30, 0), row=0, column=1, sticky=E)

        Label(frame_strat_skimage, text="Edge low threshold").grid(row=1, column=0, sticky=W)
        edge_low_skimage = StringVar(frame_strat_skimage)
        edge_low_skimage.set("0.1")
        self.spinbox_edge_low_skimage = Spinbox(frame_strat_skimage, from_=0, to=10, increment=0.01, width=4, textvariable=edge_low_skimage)
        self.spinbox_edge_low_skimage.grid(padx=(30, 0), row=1, column=1, sticky=E)

        Label(frame_strat_skimage, text="Edge high threshold").grid(row=2, column=0, sticky=W)
        edge_high_skimage = StringVar(frame_strat_skimage)
        edge_high_skimage.set("0.3")
        self.spinbox_edge_high_skimage = Spinbox(frame_strat_skimage, from_=0, to=10, increment=0.01, width=4, textvariable=edge_high_skimage)
        self.spinbox_edge_high_skimage.grid(padx=(30, 0), row=2, column=1, sticky=E)

        Label(frame_strat_skimage, text="Confidence level").grid(row=3, column=0, sticky=W)
        conf_lvl_skimage = StringVar(frame_strat_skimage)
        conf_lvl_skimage.set("0.99")
        self.spinbox_conf_lvl_skimage = Spinbox(frame_strat_skimage, from_=0, to=1, increment=0.01, width=4, textvariable=conf_lvl_skimage)
        self.spinbox_conf_lvl_skimage.grid(padx=(30, 0), row=3, column=1, sticky=E)

        Button(frame_computation, text='Run Strategy skimage', command=self.controller.on_click_run_skimage).grid(row=1, column=1, padx=10, sticky=W)

    def _frame_results(self):
        # ************ Frame Results ************ #
        frame_results = LabelFrame(self.frame_main, text="Results", padx=10, pady=10)
        frame_results.pack(side=TOP, padx=10, pady=10, fill=X)

        Label(frame_results, text="Executed Strategy: ").grid(pady=(10, 0), row=0, column=0, sticky=W)
        self.executed_strategy = StringVar(frame_results)
        self.executed_strategy.set("None")
        label_executed_strategy = Label(frame_results, textvariable=self.executed_strategy)
        label_executed_strategy.grid(pady=(10, 0), row=0, column=1)

        Label(frame_results, text="Matches found:").grid(pady=(10, 0), row=1, column=0, sticky=W)
        self.matches_found = StringVar(frame_results)
        self.matches_found.set("0")
        self.label_matches_found = Label(frame_results, textvariable=self.matches_found)
        self.label_matches_found.grid(pady=(10, 0), row=1, column=1, sticky=W)

        Button(frame_results, text='Show plot results', command=self.controller.on_click_plot_results_skimage).grid(row=2, column=0, padx=0, sticky=W)

    def _frame_image_viewer(self):
        # ************ Image viewer ************ #
        self.frame_image_viewer = LabelFrame(self.frame_main, text="Image viewer", padx=10, pady=10)
        self.frame_image_viewer.pack(side=TOP, padx=10, pady=10, fill=X)

        self.canvas_desktop_img = Canvas(self.frame_image_viewer, width=384, height=216)
        self.canvas_desktop_img.grid(row=3, column=0, sticky="WSEN")
        self.desktop_img = self.canvas_desktop_img.create_image(384/2, 216/2, image=self.haystack_img)
        self.canvas_desktop_img.bind("<Button-1>", self._img_viewer)

        self.canvas_ref_img = Canvas(self.frame_image_viewer, width=1, height=1)
        self.canvas_ref_img.grid(row=3, column=1, sticky="WSEN")
        self.ref_img = self.canvas_ref_img.create_image(47.5, 216/2, image=self.needle_img)

        Label(self.frame_image_viewer, text="Desktop").grid(pady=(0, 0), row=4, column=0, sticky="WSEN")
        Label(self.frame_image_viewer, text="Reference Image").grid(pady=(0, 0), row=4, column=1, sticky="WSEN")

    
    # ************* Bindings *************** #

    def _img_viewer(self, event=None):
        img_viewer = Toplevel(self)
        img_viewer.title("Image Viewer")
        self.haystack_img = self.image_container.get_haystack_image_orig_size(format=ImageFormat.IMAGETK)
        self.label_img_viewer = Label(img_viewer, image=self.haystack_img)
        self.label_img_viewer.pack()
