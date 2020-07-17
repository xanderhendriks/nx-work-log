import commctrl
import os
import struct
import win32api
import win32con
import win32rcparser

try:
    import winxpgui as win32gui
except ImportError:
    import win32gui


class ChangeTimeDialog():
    instance = None

    def __new__(cls):
        if not ChangeTimeDialog.instance:
            ChangeTimeDialog.instance = ChangeTimeDialog.__ChangeTimeDialog()
        return ChangeTimeDialog.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)

    class __ChangeTimeDialog():
        def __init__(self):
            self.hwnd = None
            rc_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'nx_work_log.rc')
            self.resources = win32rcparser.Parse(rc_file)
            self.minutes = 0

        def get_time(self):
            if self.hwnd is not None:
                minutes = 60 * int(win32gui.GetWindowText(win32gui.GetDlgItem(self.hwnd, self.resources.ids['IDC_HOURS'])))
                minutes += int(win32gui.GetWindowText(win32gui.GetDlgItem(self.hwnd, self.resources.ids['IDC_MINUTES'])))
                self.minutes = minutes

            return self.minutes

        def set_time(self, minutes):
            self.minutes = minutes

            if self.hwnd is not None:
                win32gui.SetWindowText(win32gui.GetDlgItem(self.hwnd, self.resources.ids['IDC_HOURS']), str(int(self.minutes / 60)))
                win32gui.SetWindowText(win32gui.GetDlgItem(self.hwnd, self.resources.ids['IDC_MINUTES']), str(self.minutes % 60))

        def show_window(self):
            if self.hwnd is None:
                self.__create_window()
            else:
                win32gui.BringWindowToTop(self.hwnd)

            win32gui.SetWindowText(win32gui.GetDlgItem(self.hwnd, self.resources.ids['IDC_HOURS']), str(int(self.minutes / 60)))
            win32gui.SetWindowText(win32gui.GetDlgItem(self.hwnd, self.resources.ids['IDC_MINUTES']), str(self.minutes % 60))

        def __create_window(self):
            message_map = {
                win32con.WM_INITDIALOG: self.__on_init_dialog,
                win32con.WM_CLOSE: self.__on_close,
                win32con.WM_COMMAND: self.__on_command,
                win32con.WM_NOTIFY: self.__on_spin_change,
            }

            win32gui.CreateDialogIndirect(0, self.resources.dialogs['IDD_CHANGE_TIME'], 0, message_map)

        def __on_init_dialog(self, hwnd, msg, wparam, lparam):
            self.hwnd = hwnd

            win32gui.SendMessage(win32gui.GetDlgItem(self.hwnd, self.resources.ids['IDC_SPIN_HOURS']), commctrl.UDM_SETPOS, 0, 5)
            win32gui.SendMessage(win32gui.GetDlgItem(self.hwnd, self.resources.ids['IDC_SPIN_HOURS']), commctrl.UDM_SETRANGE, 0,
                                 struct.unpack('L', struct.pack('hh', 10, 1))[0])
            win32gui.SendMessage(win32gui.GetDlgItem(self.hwnd, self.resources.ids['IDC_SPIN_MINUTES']), commctrl.UDM_SETPOS, 0, 5)
            win32gui.SendMessage(win32gui.GetDlgItem(self.hwnd, self.resources.ids['IDC_SPIN_MINUTES']), commctrl.UDM_SETRANGE, 0,
                                 struct.unpack('L', struct.pack('hh', 10, 1))[0])

            # centre the dialog
            desktop = win32gui.GetDesktopWindow()
            l, t, r, b = win32gui.GetWindowRect(self.hwnd)
            dt_l, dt_t, dt_r, dt_b = win32gui.GetWindowRect(desktop)
            centre_x, centre_y = win32gui.ClientToScreen(desktop, ((dt_r - dt_l) // 2, (dt_b - dt_t) // 2))
            win32gui.MoveWindow(hwnd, centre_x - (r // 2), centre_y - (b // 2), r - l, b - t, 0)

        def __on_command(self, hwnd, msg, wparam, lparam):
            id = win32api.LOWORD(wparam)
            if id in [win32con.IDOK]:
                win32gui.EndDialog(hwnd, id)

        def __on_close(self, hwnd, msg, wparam, lparam):
            id = win32api.LOWORD(wparam)
            win32gui.EndDialog(hwnd, id)
            self.hwnd = None

        def __on_spin_change(self, hwnd, msg, wparam, lparam):
            id = win32api.LOWORD(wparam)
            offset = win32api.LOWORD(win32gui.SendMessage(win32gui.GetDlgItem(self.hwnd, id), commctrl.UDM_GETPOS, 0, 0)) - 5
            win32gui.SendMessage(win32gui.GetDlgItem(self.hwnd, id), commctrl.UDM_SETPOS, 0, 5)

            if id == self.resources.ids['IDC_SPIN_HOURS']:
                time = self.get_time() + offset * 60
                self.set_time(time)
            elif id == self.resources.ids['IDC_SPIN_MINUTES']:
                time = self.get_time() + offset
                self.set_time(time)
