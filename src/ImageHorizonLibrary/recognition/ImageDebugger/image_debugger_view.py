import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
from .image_manipulation import ImageFormat


class UILocatorView(Tk):
    def __init__(self, controller, image_container, image_horizon_instance):
        super().__init__()
        self.title("ImageHorizonLibrary - Debugger")
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
        self._status_bar()

    def _frame_main(self):
        # *************** Frame Main *************** #
        self.frame_main = Frame(self)
        self.frame_main.pack(side=TOP, padx=2, pady=2)

    def _frame_load_reference_image(self):
        # ************ Frame Select image ************ #
        frame_import_ref_image = LabelFrame(self.frame_main, text="Select reference image (.png)", padx=2, pady=2)
        frame_import_ref_image.pack(side=TOP, padx=2, pady=2, fill=X)
        Label(frame_import_ref_image, text="Reference directory path:").pack(side=TOP, anchor=W)
        self.ref_dir_path = StringVar(frame_import_ref_image)
        self.label_ref_dir_path = Label(frame_import_ref_image, textvariable=self.ref_dir_path, fg='green')
        self.label_ref_dir_path.pack(side=TOP, anchor=W)
        list_needle_images_names = self.controller.create_list_of_images(self.image_horizon_instance.reference_folder)
        self.combobox_needle_img_name = ttk.Combobox(frame_import_ref_image, value=list_needle_images_names, width=10, state="readonly")
        self.combobox_needle_img_name.pack(fill=X, pady=(2,0))
        self.combobox_needle_img_name.bind("<<ComboboxSelected>>", self.controller.on_select)
    
    def _frame_computation_params(self):
        # ************ Frame Computation ************ #
        frame_computation = LabelFrame(self.frame_main, text="Computation", padx=2, pady=2)
        frame_computation.pack(side=TOP, padx=2, pady=2, fill=X)

        frame_computation.columnconfigure(0, weight=1)
        frame_computation.columnconfigure(1, weight=1)
        
        # ************ Frame Strategy pyAutogui ************* #
        frame_strat_pyautogui = LabelFrame(frame_computation, text="Strategy pyAutoGui", padx=2, pady=2)
        frame_strat_pyautogui.grid(row=0, column=0, padx=2, pady=2, sticky="WNS")

        frame_strat_pyautogui.columnconfigure(0, weight=3)
        frame_strat_pyautogui.columnconfigure(1, weight=1)

        Label(frame_strat_pyautogui, text="Confidence level").grid(row=0, column=0, sticky=W)
        self.conf_lvl_ag = StringVar(frame_strat_pyautogui)
        self.spinbox_conf_lvl_ag = Spinbox(frame_strat_pyautogui, from_=0, to=1, increment=0.01, width=4, textvariable=self.conf_lvl_ag)
        self.spinbox_conf_lvl_ag.grid(padx=(2, 0), row=0, column=1, sticky=E)

        self.btn_run_pyautogui = Button(frame_computation, text='Detect reference image', command=self.controller.on_click_run_pyautogui)
        self.btn_run_pyautogui.grid(row=1, column=0, padx=2, sticky=W)

        # ************ Frame Strategy skimage ************ #
        frame_strat_skimage = LabelFrame(frame_computation, text="Strategy skimage", padx=2, pady=2)
        frame_strat_skimage.grid(row=0, column=1, padx=2, pady=2, sticky=W)

        frame_strat_skimage.columnconfigure(0, weight=3)
        frame_strat_skimage.columnconfigure(1, weight=1)
        
        Label(frame_strat_skimage, text="Edge sigma").grid(row=0, column=0, sticky=W)
        self.edge_sigma_skimage = StringVar(frame_strat_skimage)
        self.spinbox_edge_sigma_skimage = Spinbox(frame_strat_skimage, from_=0, to=5, increment=0.01, width=4, textvariable=self.edge_sigma_skimage)
        self.spinbox_edge_sigma_skimage.grid(padx=(2, 0), row=0, column=1, sticky=E)

        Label(frame_strat_skimage, text="Edge low threshold").grid(row=1, column=0, sticky=W)
        self.edge_low_skimage = StringVar(frame_strat_skimage)
        self.spinbox_edge_low_skimage = Spinbox(frame_strat_skimage, from_=0, to=10, increment=0.01, width=4, textvariable=self.edge_low_skimage)
        self.spinbox_edge_low_skimage.grid(padx=(2, 0), row=1, column=1, sticky=E)

        Label(frame_strat_skimage, text="Edge high threshold").grid(row=2, column=0, sticky=W)
        self.edge_high_skimage = StringVar(frame_strat_skimage)
        self.spinbox_edge_high_skimage = Spinbox(frame_strat_skimage, from_=0, to=10, increment=0.01, width=4, textvariable=self.edge_high_skimage)
        self.spinbox_edge_high_skimage.grid(padx=(2, 0), row=2, column=1, sticky=E)

        Label(frame_strat_skimage, text="Confidence level").grid(row=3, column=0, sticky=W)
        self.conf_lvl_skimage = StringVar(frame_strat_skimage)
        self.spinbox_conf_lvl_skimage = Spinbox(frame_strat_skimage, from_=0, to=1, increment=0.01, width=4, textvariable=self.conf_lvl_skimage)
        self.spinbox_conf_lvl_skimage.grid(padx=(2, 0), row=3, column=1, sticky=E)

        self.btn_run_skimage = Button(frame_computation, text='Detect reference image', command=self.controller.on_click_run_skimage)
        self.btn_run_skimage.grid(row=1, column=1, padx=2, sticky=W)
        self.btn_edge_detection_debugger = Button(frame_computation, text='Edge detection debugger', command=self.controller.on_click_plot_results_skimage)
        self.btn_edge_detection_debugger.grid(row=2, column=1, padx=2, sticky=W)

    def _frame_results(self):
        # ************ Frame Results ************ #
        frame_results = LabelFrame(self.frame_main, text="Results", padx=2, pady=2)
        frame_results.pack(side=TOP, padx=2, pady=2, fill=X)

        frame_results_details = Frame(frame_results)
        frame_results_details.pack(side=TOP, fill=X)

        Label(frame_results_details, text="Executed Strategy: ").grid(pady=(2, 0), row=0, column=0, sticky=W)
        self.executed_strategy = StringVar(frame_results_details)
        label_executed_strategy = Label(frame_results_details, textvariable=self.executed_strategy)
        label_executed_strategy.grid(pady=(2, 0), row=0, column=1)
        
        Label(frame_results_details, text="Matches found:").grid(pady=(2, 0), row=1, column=0, sticky=W)
        self.matches_found = StringVar(frame_results_details)
        self.label_matches_found = Label(frame_results_details, textvariable=self.matches_found)
        self.label_matches_found.grid(pady=(2, 0), row=1, column=1, sticky=W)

        frame_snippet = Frame(frame_results)
        frame_snippet.pack(side=TOP, fill=X)
        Label(frame_snippet, text="Keyword to use this strategy:").pack(pady=(2, 0), side=TOP, anchor=W)
        self.set_strategy_snippet = StringVar(frame_snippet)
        self.label_strategy_snippet = Entry(frame_snippet, textvariable=self.set_strategy_snippet, width=75)
        self.label_strategy_snippet.pack(pady=(0, 0), side=LEFT, anchor=W)
        self.btn_copy_strategy_snippet = Button(frame_snippet, text='Copy', command=self.controller.copy_to_clipboard)
        self.btn_copy_strategy_snippet.pack(side=RIGHT, padx=(2, 0), anchor=E)

    def _frame_image_viewer(self):
        # ************ Image viewer ************ #
        self.frame_image_viewer = LabelFrame(self.frame_main, text="Image viewer", padx=2, pady=2)
        self.frame_image_viewer.pack(side=TOP, padx=2, pady=2, fill=X)

        self.canvas_desktop_img = Canvas(self.frame_image_viewer, width=384, height=216)
        self.canvas_desktop_img.grid(row=3, column=0, sticky="WSEN")
        self.desktop_img = self.canvas_desktop_img.create_image(384/2, 216/2, image=self.haystack_img)
        self.canvas_desktop_img.bind("<Button-1>", self._img_viewer)
        self.canvas_desktop_img.bind("<Enter>", self._img_viewer_hover_enter)
        self.canvas_desktop_img.bind("<Leave>", self._img_viewer_hover_leave)

        self.canvas_ref_img = Canvas(self.frame_image_viewer, width=1, height=1)
        self.canvas_ref_img.grid(row=3, column=1, sticky="WSEN")
        self.ref_img = self.canvas_ref_img.create_image(47.5, 216/2, image=self.needle_img)

        Label(self.frame_image_viewer, text="Desktop").grid(pady=(0, 0), row=4, column=0, sticky="WSEN")
        Label(self.frame_image_viewer, text="Reference Image").grid(pady=(0, 0), row=4, column=1, sticky="WSEN")

    
    # ************* Status bar *************** #
    def _status_bar(self):
        self.frame_statusBar = Frame(self)
        self.frame_statusBar.pack(side=TOP, fill=X, expand=True)
        
        self.statusOrHints = StringVar(self.frame_statusBar)

        self.statusBar = Label(self.frame_statusBar, textvariable=self.statusOrHints, bd=1, relief=SUNKEN, anchor=W)
        self.statusBar.pack(side=BOTTOM, fill=X, expand=True)

    # ************* Bindings *************** #

    def _img_viewer(self, event=None):
        img_viewer = Toplevel(self)
        img_viewer.title("Image Viewer")
        self.haystack_img = self.image_container.get_haystack_image_orig_size(format=ImageFormat.IMAGETK)
        self.label_img_viewer = Label(img_viewer, image=self.haystack_img)
        self.label_img_viewer.pack()

    def _img_viewer_hover_enter(self, event=None):
        self.statusOrHints.set("Click to view in full screen")

    def _img_viewer_hover_leave(self, event=None):
        self.statusOrHints.set("")