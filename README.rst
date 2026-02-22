NX Work Log
===========

I wrote this program originally in Borland C++ Builder. It adds an icon to the windows system tray that is green when it's
measuring time and red when it's paused. I use it to measure my working hours, so I can switch it off when doing non work
related tasks.

When I found `Simon Brunning SysTrayIcon  <http://www.brunningonline.net/simon/blog/archives/SysTrayIcon.py.html>`_ I decided
to rewrite the application in Python as I wanted to make some improvements to the tool and no longer wanted to use my outdated
version of C++ Builder.

As I was exploring the winpy32 package I found it contains a resource file parser and I thought it would be cool to define
the dialog in Microsoft Visual Studio and see how this can be used in Python.


Linux port
==========
As I'm also working on Projects requiring Ubuntu, I wanted to make the tool cross platform. 

The Linux tray implementation uses ``pystray`` and behavior depends on the backend provided by the desktop environment.

- Left/right mouse button behavior is not always identical to Windows. With the AppIndicator backend, primary click is menu-focused, so left click may open the menu instead of toggling pause.
- Hover tooltip text is often not shown by Linux shells even when the application updates the tray title.
- As a workaround for missing hover text, the current logged time is shown as the first (disabled) menu entry.
- If AppIndicator libraries are missing, the app falls back to the Xorg backend. On Xorg, menu support is limited and right-click menu entries may be unavailable.

For full tray menu support on Ubuntu, install:

.. code-block:: bash

	sudo apt update
	sudo apt install libayatana-appindicator3-1 gir1.2-ayatanaappindicator3-0.1

You can force a specific backend for troubleshooting by setting the ``PYSTRAY_BACKEND`` environment variable (for example ``appindicator`` or ``xorg``) before starting ``nxworklog``.