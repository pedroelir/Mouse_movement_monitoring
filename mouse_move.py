"""Modue that loops chmonitoring the position of the mouse."""

from typing import TypeVar

import PIL.Image

import pyautogui

import pystray


TMouseApp = TypeVar("TMouseApp", bound="MouseApp")


def monitor_mouse(time_to_monitor: int) -> None:
    """Monitor the position of the mouse if it has not moved the given time it will move it and press Caplock.

    Args:
        time_to_monitor: Ttime that will trigger mouse movement if not mouse position change was detected
    """
    old_position = pyautogui.position()
    print("Waiting 15 sec before starting to monitorng")
    pyautogui.countdown(15)
    while True:
        current_position = pyautogui.position()
        is_same_position = current_position == old_position
        print(f"{current_position=}")
        print(f"{is_same_position=}")
        old_position = current_position
        if is_same_position:
            pyautogui.moveRel(-1, 1, 0.05)
            print(pyautogui.position())
            pyautogui.moveRel(1, -1, 0.05)
            print(pyautogui.position())
            pyautogui.press("capslocK")
            pyautogui.press("capslocK")
        pyautogui.countdown(time_to_monitor)


class MouseApp:
    """Application class."""

    def __init__(self: TMouseApp) -> TMouseApp:
        """Create all needed menus, and sub menus from the app."""
        self.icon_image = PIL.Image.open("C:\\Windows\\Cursors\\lperson.cur")
        self.menu_hello = pystray.MenuItem("Say Hello", self._on_clicked)
        self.menu_start = pystray.MenuItem("Start", self._on_clicked)
        self.menu_stop = pystray.MenuItem("Exit", self._on_clicked)
        self.app_menu = pystray.Menu(self.menu_hello, self.menu_start, self.menu_stop)
        self.icon = pystray.Icon(
            "Mouse",
            self.icon_image,
            title="Mouse checker",
            menu=self.app_menu,
        )

    def run(self: TMouseApp) -> None:
        """Run application."""
        self.icon.run()  # this will run infinitely

    def _on_clicked(self: TMouseApp, icon: pystray.Icon, item: pystray.MenuItem) -> None:
        """Act when a menu item is clicked."""
        if str(item) == "Say Hello":
            print("Hello World")
        if str(item) == "Start":
            print("Start")
        if str(item) == "Exit":
            print("Exit")
            self.icon.stop()


def main() -> None:
    """Run Main function."""
    mapp = MouseApp()
    mapp.run()


if __name__ == "__main__":
    main()
