# -*- coding: utf-8 -*-
from collections import OrderedDict
from contextlib import contextmanager
import inspect

from .errors import *    # import errors before checking dependencies!

try:
    import pyautogui as ag
except ImportError:
    raise ImageHorizonLibraryError('There is something wrong with pyautogui or '
                                   'it is not installed.')

try:
    from robot.api import logger as LOGGER
    from robot.libraries.BuiltIn import BuiltIn
except ImportError:
    raise ImageHorizonLibraryError('There is something wrong with '
                                   'Robot Framework or it is not installed.')

try:
    from tkinter import Tk as TK
except ImportError:
    raise ImageHorizonLibraryError('There is either something wrong with '
                                   'Tkinter or you are running this on Java, '
                                   'which is not a supported platform. Please '
                                   'use Python and verify that Tkinter works.')

try:
    import skimage as sk
except ImportError: 
    raise ImageHorizonLibraryError('There is either something wrong with skimage '
                                    '(scikit-image) or it is not installed.')

from . import utils
from .interaction import *
from .recognition import *
from .version import VERSION

__version__ = VERSION

class ImageHorizonLibrary(_Keyboard, _Mouse, _OperatingSystem, _Screenshot):
    '''A cross-platform Robot Framework library for GUI automation.

    ImageHorizonLibrary provides keyboard and mouse actions as well as
    facilities to recognize images on screen. It can also take screenshots in
    case of failure or otherwise.


    This library is built on top of
    [https://pyautogui.readthedocs.org|pyautogui] and
    [https://scikit-image.org|scikit-image]

    = Image Recognition = 

    == Reference image names ==
    ``reference_image`` parameter can be either a single file, or a folder.
    If ``reference_image`` is a folder, image recognition is tried separately
    for each image in that folder, in alphabetical order until a match is found.

    For ease of use, reference image names are automatically normalized
    according to the following rules:

    - The name is lower cased: ``MYPICTURE`` and ``mYPiCtUrE`` become
      ``mypicture``

    - All spaces are converted to underscore ``_``: ``my picture`` becomes
      ``my_picture``

    - If the image name does not end in ``.png``, it will be added:
      ``mypicture`` becomes ``mypicture.png``

    - Path to _reference folder_ is prepended. This option must be given when
      `importing` the library.

    Using good names for reference images is evident from easy-to-read test
    data:

    | `Import Library` | ImageHorizonLibrary                   | reference_folder=images |                                                            |
    | `Click Image`    | popup Window title                    |                         | # Path is images/popup_window_title.png                    |
    | `Click Image`    | button Login Without User Credentials |                         | # Path is images/button_login_without_user_credentials.png |

    == Handling Recognition problems ==
    By default, image recognition in ImageHorizonLibrary is done with ``pyautogui``
    which always expects a pixel-perfect matching between the reference image and
    a region on th screen. 

    Problems can arise when

    - the application's GUI has transpareny effects
    - the screen resolution/the window size changes
    - font aliasing is used for dynamic text
    - compression algorithms in RDP/Citrix cause invisible artifacts
    - ...and many more situations.
    
    ImageHorizon comes with a parameter ``confidence level`` which allows to
    adjust the precision manually and make the recognition more "greedy".

    Confidence level can be set during `library importing` and during the test 
    case with keyword `Set Confidence` to a decimal value between 0 and 1 
    (inclusive). It changes the image recognition results depending on the
    recognition strategies: 
    - ``pyautogui`` (default)
    - ``skimage``
    
    === Confidence Level (pyautogui) ===
    Confidence level in strategy ``pyautogui`` is a decimal value between
    0 and 1 (inclusive) and defines how many percent of the reference image pixels
    must match the found region's image (1=100%=default).

    If you do not encouner any recognition problems or only a small amount of
    pixels vary, ``pyautogui`` with confidence is the right choice. 

    To use confidence level in mode ``pyautogui`` the 
    [https://pypi.org/project/opencv-python|opencv-python] Python package
    must be installed separately:

    | $ pip install opencv-python

    After installation, the library will use OpenCV, which enables setting the
    


    = Performance =

    Locating images on screen, especially if screen resolution is large and
    reference image is also large, might take considerable time. It is
    therefore advisable to save the returned coordinates if you are
    manipulating the same context many times in the row:

    | `Wait For`                   | label Name |     |
    | `Click To The Left Of Image` | label Name | 200 |

    In the above example, same image is located twice. Below is an example how
    we can leverage the returned location:

    | ${location}=           | `Wait For`  | label Name |
    | `Click To The Left Of` | ${location} | 200        |
    '''    

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self, reference_folder=None, screenshot_folder=None,
                 keyword_on_failure='ImageHorizonLibrary.Take A Screenshot',
                 confidence=None, strategy='pyautogui', 
                 edge_sigma=2.0, edge_low_threshold=0.1, edge_high_threshold=0.3):
        '''ImageHorizonLibrary can be imported with several options.
        
        ``reference_folder`` is path to the folder where all reference images
        are stored. It must be a _valid absolute path_. As the library
        is suite-specific (ie. new instance is created for every suite),
        different suites can have different folders for it's reference images.

        ``screenshot_folder`` is path to the folder where screenshots are
        saved. If not given, screenshots are saved to the current working
        directory.

        ``keyword_on_failure`` is the keyword to be run, when location-related
        keywords fail. If you wish to not take screenshots, use for example
        `BuiltIn.No Operation`. Keyword must however be a valid keyword.
        
        ``strategy`` sets the way how images are detected on the screen. 
        - `pyautogui` - (Default)
        - `skimage` - Advanced image recognition options with canny edge detection
          - `edge_sigma` - Gaussian blur intensity
          - `edge_low_threshold` - low pixel gradient threshold
          - `edge_high_threshold` - high pixel gradient threshold
        '''
                
        # _RecognizeImages.set_strategy(self, strategy)
        self.reference_folder = reference_folder
        self.screenshot_folder = screenshot_folder
        self.keyword_on_failure = keyword_on_failure
        self.open_applications = OrderedDict()
        self.screenshot_counter = 1
        self.is_windows = utils.is_windows()
        self.is_mac = utils.is_mac()
        self.is_linux = utils.is_linux()
        self.has_retina = utils.has_retina()
        self.has_cv = utils.has_cv()
        self.has_skimage = utils.has_skimage()
        self.confidence = confidence
        self._class_bases = inspect.getmro(self.__class__)
        self.set_strategy(strategy)
        self.edge_sigma = edge_sigma
        self.edge_low_threshold = edge_low_threshold
        self.edge_high_threshold = edge_high_threshold



    def set_strategy(self, strategy, edge_sigma=2.0, edge_low_threshold=0.1, edge_high_threshold=0.3):
        '''Sets the way how images are detected on the screen. 
        
        `strategy` is either one of the values: 
        - `pyautogui` - (Default)
        - `skimage` - Advanced image recognition options with canny edge detection
        '''
        self.strategy = strategy
        if strategy == 'pyautogui':
            strategy_cls = _StrategyPyautogui
        elif strategy == 'skimage': 
            strategy_cls = _StrategySkimage
            self.edge_sigma = edge_sigma
            self.edge_low_threshold = edge_low_threshold
            self.edge_high_threshold = edge_high_threshold
        else: 
            raise StrategyException('Invalid strategy: "%s"' % strategy)
            
        # The challenge here is to replace a superclass of an already existing object.
        # Base classes of the new strategy superclass (+ its superclasses in turn)
        strategy_bases = inspect.getmro(strategy_cls)
        # The base classes of self (saved once during init) get expanded with the strategy's base classes
        new_bases = tuple([item for item in strategy_bases if item not in self._class_bases]) + self._class_bases
        # Now construct a new class: keep its name, use the new bases and duplicate its namespace
        new_class = type(self.__class__.__name__, new_bases, self.__dict__.copy())
        # Give self a new identity
        self.__class__ = new_class
        # Effects when switching to $strategy: 
        # - edge_* params change (only for skimage and only if set)
        # - self.strategd == '$strategy'
        # - self._locate gets a bound method of _Strategy$strategy._locate 
        


    def _get_location(self, direction, location, offset):
        x, y = location
        offset = int(offset)
        if direction == 'left':
            x = x - offset
        if direction == 'up':
            y = y - offset
        if direction == 'right':
            x = x + offset
        if direction == 'down':
            y = y + offset
        return x, y

    def _click_to_the_direction_of(self, direction, location, offset,
                                   clicks, button, interval):
        x, y = self._get_location(direction, location, offset)
        try:
            clicks = int(clicks)
        except ValueError:
            raise MouseException('Invalid argument "%s" for `clicks`')
        if button not in ['left', 'middle', 'right']:
            raise MouseException('Invalid button "%s" for `button`')
        try:
            interval = float(interval)
        except ValueError:
            raise MouseException('Invalid argument "%s" for `interval`')

        LOGGER.info('Clicking %d time(s) at (%d, %d) with '
                    '%s mouse button at interval %f' % (clicks, x, y,
                                                        button, interval))
        ag.click(x, y, clicks=clicks, button=button, interval=interval)

    def _convert_to_valid_special_key(self, key):
        key = str(key).lower()
        if key.startswith('key.'):
            key = key.split('key.', 1)[1]
        elif len(key) > 1:
            return None
        if key in ag.KEYBOARD_KEYS:
            return key
        return None

    def _validate_keys(self, keys):
        valid_keys = []
        for key in keys:
            valid_key = self._convert_to_valid_special_key(key)
            if not valid_key:
                raise KeyboardException('Invalid keyboard key "%s", valid '
                                        'keyboard keys are:\n%r' %
                                        (key, ', '.join(ag.KEYBOARD_KEYS)))
            valid_keys.append(valid_key)
        return valid_keys

    def _press(self, *keys, **options):
        keys = self._validate_keys(keys)
        ag.hotkey(*keys, **options)

    @contextmanager
    def _tk(self):
        tk = TK()
        yield tk.clipboard_get()
        tk.destroy()

    def copy(self):
        '''Executes ``Ctrl+C`` on Windows and Linux, ``⌘+C`` on OS X and
        returns the content of the clipboard.'''
        key = 'Key.command' if self.is_mac else 'Key.ctrl'
        self._press(key, 'c')
        return self.get_clipboard_content()

    def get_clipboard_content(self):
        '''Returns what is currently copied in the system clipboard.'''
        with self._tk() as clipboard_content:
            return clipboard_content

    def pause(self):
        '''Shows a dialog that must be dismissed with manually clicking.

        This is mainly for when you are developing the test case and want to
        stop the test execution.

        It should probably not be used otherwise.
        '''
        ag.alert(text='Test execution paused.', title='Pause',
                 button='Continue')

    def _run_on_failure(self):
        if not self.keyword_on_failure:
            return
        try:
            BuiltIn().run_keyword(self.keyword_on_failure)
        except Exception as e:
            LOGGER.debug(e)
            LOGGER.warn('Failed to take a screenshot. '
                        'Is Robot Framework running?')

    def set_reference_folder(self, reference_folder_path):
        '''Sets where all reference images are stored.

        See `library importing` for format of the reference folder path.
        '''
        self.reference_folder = reference_folder_path

    def set_screenshot_folder(self, screenshot_folder_path):
        '''Sets the folder where screenshots are saved to.

        See `library importing` for more specific information.
        '''
        self.screenshot_folder = screenshot_folder_path

    def set_confidence(self, new_confidence):
        '''Sets the accuracy when finding images.

        ``new_confidence`` is a decimal number between 0 and 1 inclusive.

        See `Confidence level` about additional dependencies that needs to be
        installed before this keyword has any effect.
        '''
        if new_confidence is not None:
            try:
                new_confidence = float(new_confidence)
                if not 1 >= new_confidence >= 0:
                    LOGGER.warn('Unable to set confidence to {}. Value '
                                'must be between 0 and 1, inclusive.'
                                .format(new_confidence))
                else:
                    self.confidence = new_confidence
            except TypeError as err:
                LOGGER.warn("Can't set confidence to {}".format(new_confidence))
        else:
            self.confidence = None

