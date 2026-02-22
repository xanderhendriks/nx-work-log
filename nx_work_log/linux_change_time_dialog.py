import tkinter as tk
import threading


class ChangeTimeDialog():
    """
    Singleton class providing the dialog to change the time using tkinter on Linux

    .. document private classes
    .. automethod:: __ChangeTimeDialog
    """
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
        """
        Internal class implementing the change time dialog using tkinter
        """

        def __init__(self):
            self.minutes = 0
            self.time_changed_callback = None
            self._dialog_open = False

        def get_time(self):
            """
            Get the current logged number of minutes
            :return: Number of minutes
            """
            return self.minutes

        def set_time(self, minutes):
            """
            Set the current logged number of minutes
            :param minutes: Number of minutes
            """
            self.minutes = minutes

            if self.time_changed_callback is not None:
                self.time_changed_callback(minutes)

        def set_time_changed_callback(self, time_changed_callback):
            """
            Set the callback function for time changes
            :param time_changed_callback: Callback function
            """
            self.time_changed_callback = time_changed_callback

        def show_window(self):
            """
            Show the change time dialog window
            """
            if self._dialog_open:
                return

            thread = threading.Thread(target=self._show_dialog, daemon=True)
            thread.start()

        def _show_dialog(self):
            self._dialog_open = True
            try:
                root = tk.Tk()
                root.title("Change Time")
                root.resizable(False, False)

                hours_var = tk.StringVar(value=str(int(self.minutes / 60)))
                minutes_var = tk.StringVar(value=str(self.minutes % 60))

                frame = tk.Frame(root, padx=10, pady=10)
                frame.pack()

                tk.Label(frame, text="Hours:").grid(row=0, column=0)
                tk.Spinbox(frame, from_=0, to=999, textvariable=hours_var, width=5).grid(row=0, column=1, padx=5)

                tk.Label(frame, text="Minutes:").grid(row=0, column=2)
                tk.Spinbox(frame, from_=0, to=59, textvariable=minutes_var, width=5).grid(row=0, column=3, padx=5)

                def on_ok():
                    try:
                        h = int(hours_var.get())
                        m = int(minutes_var.get())
                        self.set_time(h * 60 + m)
                    except ValueError:
                        pass
                    root.destroy()

                tk.Button(frame, text="OK", command=on_ok).grid(row=1, column=0, columnspan=4, pady=(10, 0))

                root.protocol("WM_DELETE_WINDOW", on_ok)

                # Centre the window on screen
                root.update_idletasks()
                x = (root.winfo_screenwidth() - root.winfo_reqwidth()) // 2
                y = (root.winfo_screenheight() - root.winfo_reqheight()) // 2
                root.geometry("+{}+{}".format(x, y))

                root.mainloop()
            finally:
                self._dialog_open = False
