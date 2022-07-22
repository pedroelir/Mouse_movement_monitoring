"""Modue that loops chmonitoring the position of the mouse."""

import PIL.Image

import pyautogui

import pystray


def on_clicked(icon: pystray.Icon, item: pystray.MenuItem) -> None:
    """Act when a menu item is clicked."""
    if str(item) == "Say Hello":
        print("Hello World")
    if str(item) == "Start":
        print("Start")
    if str(item) == "Exit":
        print("Exit")
        icon.stop()


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


def main() -> None:
    """Run Main function."""
    icon_image = PIL.Image.open("C:\\Windows\\Cursors\\lperson.cur")
    menu_hello = pystray.MenuItem("Say Hello", on_clicked)
    menu_start = pystray.MenuItem("Start", on_clicked)
    menu_stop = pystray.MenuItem("Stop", on_clicked)
    app_menu = pystray.Menu(menu_hello, menu_start, menu_stop)
    icon = pystray.Icon(
        "Mouse",
        icon_image,
        title="Mouse checker",
        menu=app_menu,
    )
    icon.run()


if __name__ == "__main__":
    main()
