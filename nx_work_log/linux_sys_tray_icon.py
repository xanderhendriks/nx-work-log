import os

if 'PYSTRAY_BACKEND' not in os.environ:
    try:
        import gi
        try:
            gi.require_version('AyatanaAppIndicator3', '0.1')
        except ValueError:
            gi.require_version('AppIndicator3', '0.1')
        os.environ['PYSTRAY_BACKEND'] = 'appindicator'
    except (ImportError, ValueError):
        os.environ['PYSTRAY_BACKEND'] = 'xorg'

from PIL import Image
import pystray


class SysTrayIcon(object):
    EXIT = 'EXIT'

    @staticmethod
    def _create_action(action_func, sys_tray_icon):
        def action(_icon, _item):
            action_func(sys_tray_icon)
        return action

    @staticmethod
    def _create_checked(check_func):
        def checked(_item):
            return check_func()
        return checked

    def _status_menu_text(self, _item):
        return self.hover_text

    def __init__(self, icon, hover_text, menu_options, on_exit=None, default_menu_index=None, window_class_name=None, call_on_startup=None):
        """
        The SysTrayIcon class implements an icon in the Linux system tray using pystray, which allows left click on the icon for an action
        and right click for a menu
        :param icon: Full path to icon file
        :param hover_text: Text to show when hovering above icon
        :param menu_options: List of menu options and functions to call
        :param on_exit: Function to call when exiting
        :param default_menu_index: The menu item to select when clicking the icon
        :param window_class_name: Unused on Linux, kept for API compatibility
        :param call_on_startup: Function to call on startup
        """
        self.icon = icon
        self.hover_text = hover_text
        self.on_exit = on_exit
        self.default_menu_index = default_menu_index or 0
        self._pystray_icon = None

        menu_items = [
            pystray.MenuItem(self._status_menu_text, None, enabled=False)
        ]
        for idx, (option_text, option_icon, option_action) in enumerate(menu_options):
            is_default = (idx == self.default_menu_index)
            if callable(option_icon):
                check_func = option_icon
                action_func = option_action
                menu_items.append(pystray.MenuItem(
                    option_text,
                    self._create_action(action_func, self),
                    checked=self._create_checked(check_func),
                    default=is_default
                ))
            else:
                action_func = option_action
                menu_items.append(pystray.MenuItem(
                    option_text,
                    self._create_action(action_func, self),
                    default=is_default
                ))

        menu_items.append(pystray.MenuItem('Exit', lambda _icon, _item: self._exit()))

        image = Image.open(self.icon)
        image.load()
        self._pystray_icon = pystray.Icon(
            "nxworklog",
            image,
            self.hover_text,
            menu=pystray.Menu(*menu_items)
        )

        def setup(tray_icon):
            tray_icon.visible = True
            if call_on_startup is not None:
                call_on_startup(self)

        self._pystray_icon.run(setup=setup)

    def refresh_icon(self):
        """
        Refresh the icon. To be called after updating the icon.
        """
        if self._pystray_icon is not None:
            image = Image.open(self.icon)
            image.load()
            self._pystray_icon.icon = image
            self._pystray_icon.title = self.hover_text

    def set_hover_text(self, hover_text):
        """
        Set the hover text for the system tray icon.
        :param hover_text: Text to display on hover
        """
        self.hover_text = hover_text
        if self._pystray_icon is not None:
            self._pystray_icon.title = hover_text
            self._pystray_icon.update_menu()

    def exit(self):
        """
        Exit the system tray icon.
        """
        self._exit()

    def _exit(self):
        if self.on_exit:
            self.on_exit(self)
        if self._pystray_icon is not None:
            self._pystray_icon.stop()
