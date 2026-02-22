from PIL import Image
import pystray


class SysTrayIcon(object):
    EXIT = 'EXIT'

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

        menu_items = []
        for idx, (option_text, option_icon, option_action) in enumerate(menu_options):
            is_default = (idx == self.default_menu_index)
            if callable(option_icon):
                check_func = option_icon
                action_func = option_action
                menu_items.append(pystray.MenuItem(
                    option_text,
                    lambda _icon, _item, f=action_func: f(self),
                    checked=lambda _item, f=check_func: f(),
                    default=is_default
                ))
            else:
                action_func = option_action
                menu_items.append(pystray.MenuItem(
                    option_text,
                    lambda _icon, _item, f=action_func: f(self),
                    default=is_default
                ))

        menu_items.append(pystray.MenuItem('Exit', lambda _icon, _item: self._exit()))

        image = Image.open(self.icon)
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
            self._pystray_icon.icon = Image.open(self.icon)
            self._pystray_icon.title = self.hover_text

    def set_hover_text(self, hover_text):
        """
        Set the hover text for the system tray icon.
        :param hover_text: Text to display on hover
        """
        self.hover_text = hover_text
        if self._pystray_icon is not None:
            self._pystray_icon.title = hover_text

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
