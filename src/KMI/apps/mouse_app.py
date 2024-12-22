"""Modue that loops chmonitoring the position of the mouse."""
import threading
import time
from typing import TypeVar

from PIL import Image

import pyautogui

from pystray import Icon, Menu, MenuItem

from winotify import Notification

from KMI import logger

TMouseApp = TypeVar("TMouseApp", bound="MouseApp")


class MouseApp:
    """Application class."""

    def __init__(self: TMouseApp, time_to_monitor: int = 120) -> TMouseApp:
        """Create all needed menus, and sub menus from the app."""
        self.icon_image: Image = Image.open("C:\\Windows\\Cursors\\lperson.cur")
        self.menu_hello: MenuItem = MenuItem("Say Hello", self._say_hello)
        self.menu_start: MenuItem = MenuItem("Start", self._start)
        self.menu_pause: MenuItem = MenuItem("Pause", self._pause)
        self.menu_exit: MenuItem = MenuItem("Exit", self._exit)
        self.app_menu: Menu = Menu(self.menu_hello, self.menu_start, self.menu_pause, self.menu_exit)
        self.icon: Icon = Icon(
            "KMI Settings",
            self.icon_image,
            title="KMI Settings",
            menu=self.app_menu,
        )
        self.time_to_monitor: int = time_to_monitor
        self.thread: threading.Thread = None
        self.continue_run: bool = False
        self.toast: Notification = Notification("KMI", "KMI Settings", "Hello there, Have great day at work! :)")
        self._start(self.icon, self.app_menu)

    def run(self: TMouseApp) -> None:
        """Run application."""
        self.icon.run()  # this will run infinitely

    def monitor_mouse(self: TMouseApp, time_to_monitor: int) -> None:
        """Monitor the position of the mouse if it has not moved the given time it will move it and press Caplock.

        Args:
            time_to_monitor: Ttime that will trigger mouse movement if not mouse position change was detected
        """
        old_position: pyautogui.Point = pyautogui.position()
        logger.info("Waiting 5 sec before starting to monitor")
        pyautogui.countdown(5)
        reference_time: float = time.monotonic()
        timeout: bool = False
        while self.continue_run and (not timeout):
            current_position: pyautogui.Point = pyautogui.position()
            is_same_position: bool = current_position == old_position
            logger.debug(f"{current_position=}")
            logger.debug(f"{is_same_position=}")
            old_position = current_position
            current_time: float = time.monotonic()
            time_passed: float = current_time - reference_time
            print(f"Time passed since last position changed: {int(time_passed)}", end="\r")
            timeout = time_passed > time_to_monitor
            if is_same_position and timeout:
                print("\n")
                logger.info(f"No mouse movement for {self.time_to_monitor}s, Action taken")
                pyautogui.moveRel(-1, 1, 0.05)
                logger.info(pyautogui.position())
                pyautogui.moveRel(1, -1, 0.05)
                logger.info(pyautogui.position())
                pyautogui.press("shift")
                reference_time = time.monotonic()
                timeout = False
            elif not is_same_position:
                reference_time = time.monotonic()
                timeout = False
            time.sleep(1)

    def _on_clicked(self: TMouseApp, icon: Icon, item: MenuItem) -> None:
        """Act when a menu item is clicked."""
        print("Hello World")

    def _say_hello(self: TMouseApp, icon: Icon, item: MenuItem) -> None:
        self.toast.show()

    def _start(self: TMouseApp, icon: Icon, item: MenuItem) -> None:
        self.continue_run = True
        if self.thread is None:
            self.thread = threading.Thread(target=self.monitor_mouse, args=[self.time_to_monitor])
            print("\n")
            logger.info("Starting...")
            self.thread.start()

    def _pause(self: TMouseApp, icon: Icon, item: MenuItem) -> None:
        print("\n")
        logger.info("Pause")
        self.continue_run = False
        if self.thread:
            self.thread.join(300)
            self.thread = None

    def _exit(self: TMouseApp, icon: Icon, item: MenuItem) -> None:
        print("\n")
        logger.info("Exit")
        self.continue_run = False
        if self.thread:
            self.thread.join(300)
            self.thread = None
        self.icon.stop()
