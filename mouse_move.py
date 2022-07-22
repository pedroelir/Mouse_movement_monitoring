"""Modue that loops chmonitoring the position of the mouse."""
import threading
import time
from typing import TypeVar

import PIL.Image

import pyautogui

import pystray

from winotify import Notification

TMouseApp = TypeVar("TMouseApp", bound="MouseApp")


class MouseApp:
    """Application class."""

    def __init__(self: TMouseApp, time_to_monitor: int = 120, show_position: bool = False) -> TMouseApp:
        """Create all needed menus, and sub menus from the app."""
        self.icon_image = PIL.Image.open("C:\\Windows\\Cursors\\lperson.cur")
        self.menu_hello = pystray.MenuItem("Say Hello", self._say_hello)
        self.menu_start = pystray.MenuItem("Start", self._start)
        self.menu_pause = pystray.MenuItem("Pause", self._pause)
        self.menu_exit = pystray.MenuItem("Exit", self._exit)
        self.app_menu = pystray.Menu(self.menu_hello, self.menu_start, self.menu_pause, self.menu_exit)
        self.icon = pystray.Icon(
            "KMI Settings",
            self.icon_image,
            title="KMI Settings",
            menu=self.app_menu,
        )
        self.time_to_monitor = time_to_monitor
        self.show_position = show_position
        self.t = None
        self.continue_run = False
        self.toast = Notification("KMI", "KMI Settings", "Hello there, Have great day at work! :)")
        self._start()

    def run(self: TMouseApp) -> None:
        """Run application."""
        self.icon.run()  # this will run infinitely

    def monitor_mouse(self: TMouseApp, time_to_monitor: int) -> None:
        """Monitor the position of the mouse if it has not moved the given time it will move it and press Caplock.

        Args:
            time_to_monitor: Ttime that will trigger mouse movement if not mouse position change was detected
        """
        old_position = pyautogui.position()
        print("Waiting 5 sec before starting to monitor")
        pyautogui.countdown(5)
        reference_time = time.monotonic()
        timeout = False
        while self.continue_run and (not timeout):
            current_position = pyautogui.position()
            is_same_position = current_position == old_position
            if self.show_position:
                print(f"{current_position=}")
                print(f"{is_same_position=}")
            old_position = current_position
            current_time = time.monotonic()
            time_passed = current_time - reference_time
            print(f"Time passed since last position changed: {int(time_passed)}")
            timeout = time_passed > time_to_monitor
            if is_same_position and timeout:
                print(f"No mouse movement for {self.time_to_monitor}s, Action taken")
                pyautogui.moveRel(-1, 1, 0.05)
                if self.show_position:
                    print(pyautogui.position())
                pyautogui.moveRel(1, -1, 0.05)
                if self.show_position:
                    print(pyautogui.position())
                pyautogui.press("capslocK")
                pyautogui.press("capslocK")
                reference_time = time.monotonic()
                timeout = False
            elif not is_same_position:
                reference_time = time.monotonic()
                timeout = False
            time.sleep(1)

    def _on_clicked(self: TMouseApp, icon: pystray.Icon, item: pystray.MenuItem) -> None:
        """Act when a menu item is clicked."""
        print("Hello World")

    def _say_hello(self) -> None:
        self.toast.show()

    def _start(self) -> None:
        self.continue_run = True
        if self.t is None:
            self.t = threading.Thread(target=self.monitor_mouse, args=[self.time_to_monitor])
            print("Starting...")
            self.t.start()

    def _pause(self) -> None:
        print("Pause")
        self.continue_run = False
        if self.t:
            self.t.join(300)
            self.t = None

    def _exit(self) -> None:
        print("Exit")
        self.continue_run = False
        if self.t:
            self.t.join(300)
            self.t = None
        self.icon.stop()


def main() -> None:
    """Run Main function."""
    mapp = MouseApp()
    mapp.run()


if __name__ == "__main__":
    main()
