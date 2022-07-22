"""Modue that loops chmonitoring the position of the mouse."""
import threading
import time
from typing import TypeVar

import PIL.Image

import pyautogui

import pystray


TMouseApp = TypeVar("TMouseApp", bound="MouseApp")


class MouseApp:
    """Application class."""

    def __init__(self: TMouseApp) -> TMouseApp:
        """Create all needed menus, and sub menus from the app."""
        self.icon_image = PIL.Image.open("C:\\Windows\\Cursors\\lperson.cur")
        self.menu_hello = pystray.MenuItem("Say Hello", self._on_clicked)
        self.menu_start = pystray.MenuItem("Start", self._start)
        self.menu_pause = pystray.MenuItem("Pause", self._pause)
        self.menu_exit = pystray.MenuItem("Exit", self._exit)
        self.app_menu = pystray.Menu(self.menu_hello, self.menu_start, self.menu_pause, self.menu_exit)
        self.icon = pystray.Icon(
            "Mouse",
            self.icon_image,
            title="Mouse checker",
            menu=self.app_menu,
        )
        self.t = None
        self.continue_run = False

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
            print(f"{current_position=}")
            print(f"{is_same_position=}")
            old_position = current_position
            current_time = time.monotonic()
            time_passed = current_time - reference_time
            print(f"Time passed: {int(time_passed)}")
            timeout = time_passed > time_to_monitor
            if is_same_position and timeout:
                pyautogui.moveRel(-1, 1, 0.05)
                print(pyautogui.position())
                pyautogui.moveRel(1, -1, 0.05)
                print(pyautogui.position())
                pyautogui.press("capslocK")
                pyautogui.press("capslocK")
                reference_time = time.monotonic()
                timeout = False
            elif not is_same_position:
                reference_time = time.monotonic()
            time.sleep(1)

    def _on_clicked(self: TMouseApp, icon: pystray.Icon, item: pystray.MenuItem) -> None:
        """Act when a menu item is clicked."""
        if str(item) == "Say Hello":
            print("Hello World")

    def _start(self):
        print("Start")
        self.continue_run = True
        if self.t:
            if not self.t.is_alive():
                self.t.start()
        else:
            self.t = threading.Thread(target=self.monitor_mouse, args=[15])
            self.t.start()

    def _pause(self):
        print("Pause")
        self.continue_run = False
        if self.t:
            self.t.join(300)
            self.t = None

    def _exit(self):
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
